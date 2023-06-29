# Django
from django.db import models
from django.db.models.query import QuerySet
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import (
    BaseUserManager,
    AbstractBaseUser,
)
from django.core.validators import MinLengthValidator
from django.utils import timezone

# Python
import datetime
import typing as t

# Third-party
from abstracts.models import (
    AbstractModel,
    AbstractManager,
)


class UserManager(BaseUserManager, AbstractManager):
    """
    Manager for custom create methods for user model.
    """

    def create_superuser(self, email: str, first_name: str,
                         last_name: str, password: str) -> 'User':
        """
        Create super user method.
        """
        u: User = User(email=email, first_name=first_name,
                       last_name=last_name, password=password)
        u.is_superuser = True
        u.is_active = True
        u.is_staff = True
        u.save(using=self._db)
        return u

    def create_user(self, email: str, first_name: str,
                    last_name: str, password: str,
                    password2: str) -> 'User':
        """
        Create default user method.
        """
        u: User = User(email=email, first_name=first_name,
                       last_name=last_name, password=password,
                       password2=password2)
        u.save(using=self._db)
        return u

    def get_user_or_none(self, **filter: t.Any) -> 'User':
        """
        Get user or None by field.
        """
        try:
            user: User = self.get(**filter)
        except User.DoesNotExist:
            user = None
        finally:
            return user


class User(PermissionsMixin, AbstractBaseUser, AbstractModel):
    """
    Custom model of user.
    """

    # All possible genders of user
    MALE: int = 1
    FEMALE: int = 2
    GENDERS: tuple = (
        (MALE, 'male'),
        (FEMALE, 'female'),
    )
    # Name of user
    first_name: str = models.CharField(
        verbose_name='name',
        max_length=40
    )
    # Surname of user
    last_name: str = models.CharField(
        verbose_name='surname',
        max_length=40
    )
    # Email of user to use it then in registration and logging in
    email: str = models.CharField(
        verbose_name='email',
        max_length=60,
        unique=True
    )
    # Password. Hashed in signals.py upon creation
    password: str = models.CharField(
        verbose_name='password',
        max_length=128,
        validators=(
            MinLengthValidator(7),
        )
    )
    # Password2 to make sure, if the user entered the correct password
    password2: str = models.CharField(
        verbose_name='password2',
        max_length=128,
        validators=(
            MinLengthValidator(7),
        )
    )
    # Gender of user
    gender: int = models.SmallIntegerField(
        verbose_name='gender',
        choices=GENDERS,
        null=True
    )
    # If user accout is confirmed to use it
    is_active: bool = models.BooleanField(
        verbose_name='is active',
        default=False
    )
    # If user has admin privilege
    is_staff: bool = models.BooleanField(
        verbose_name='is staff',
        default=False
    )
    is_superuser: bool = models.BooleanField(
        verbose_name='is superuser',
        default=False
    )
    USERNAME_FIELD: str = 'email'
    REQUIRED_FIELDS: tuple = (
        'first_name',
        'last_name',
        'password'
    )
    # User manager
    objects: UserManager = UserManager()

    # Get user last name + first name
    @property
    def fullname(self) -> str:
        return '%s %s' % (self.last_name, self.first_name)

    # Check if user has admin privelege
    @property
    def is_admin(self) -> bool:
        """
        Used for superuser authentication.
        """
        return self.is_active and self.is_superuser and self.is_staff

    def __repr__(self) -> str:
        return self.fullname

    class Meta:
        ordering = (
            'datetime_created',
        )
        verbose_name = 'user'
        verbose_name_plural = 'users'


class CodeManager(models.Manager):
    """
    Codes manager.
    """

    def extended_filter(self, expired: bool,
                        **kwargs: dict) -> QuerySet['AccountCode']:
        # Filter, that allows to check if code lifetime has expired
        now: datetime.datetime = timezone.now()

        queryset: QuerySet['AccountCode'] = self.filter(**kwargs)

        # If check date expire is True
        if expired is True:
            queryset = queryset.filter(datetime_expire__lt=now)

        # Otherwise
        else:
            queryset = queryset.filter(datetime_expire__gt=now)

        return queryset


class AccountCode(models.Model):
    """
    Code for users to confirm different actions.
    """

    # Length of activation code
    CODE_LENGTH: int = 6
    # Code lifetime. Will be removed from the database over time
    LIFETIME: datetime.timedelta = datetime.timedelta(minutes=10)
    # Activation-account code
    ACCOUNT_ACTIVATION: str = 1
    # Password-reset code
    PASSWORD_RESET: str = 2
    # All choices of type, that code can be
    types: tuple = (
        (ACCOUNT_ACTIVATION, 'ACCOUNT-ACTIVATION'),
        (PASSWORD_RESET, 'PASSWORD-RESET'),
    )
    # Which user the code belongs to
    code_type: str = models.PositiveSmallIntegerField(
        verbose_name='type of code',
        choices=types,
        default=ACCOUNT_ACTIVATION
    )
    user: User = models.ForeignKey(
        verbose_name='user',
        to=User,
        on_delete=models.CASCADE,
        related_name='activate_account_codes',
        null=True
    )
    # Unique=True is not used, because there are 59^50 code variations
    # for one user, which, even if repeated, will not break the server,
    # unlike the situation, if the unique=True was set
    code: str = models.CharField(
        verbose_name='code',
        max_length=CODE_LENGTH,
        validators=(
            MinLengthValidator(CODE_LENGTH),
        )
    )
    # Datetime, when code is, when code is considered expired
    datetime_expire: datetime.datetime = models.DateTimeField(
        verbose_name='expire datetime',
        default=timezone.now() + LIFETIME
    )
    # Activation code manager
    objects: CodeManager = CodeManager()


class RefreshTokenManager(AbstractManager):
    """
    Manager for refresh tokens.
    """

    def find_valid(self, token: str, fingerprint: str,
                   ip: str, user: User = None) -> QuerySet['TokenWhiteList']:
        """
        Find all valid tokens.
        """
        # Check if token is not expired
        queryset: QuerySet['TokenWhiteList'] =\
            TokenWhiteList.objects.filter(expire_datetime__gt=timezone.now())

        # If there is need to find active refresh token for user
        if user:
            queryset = queryset.filter(user=user, refresh_token=token,
                                       fingerprint=fingerprint, ip=ip)

        return queryset


class TokenWhiteList(AbstractModel):
    """
    Model for refresh tokens.
    """

    # Related user
    user: User = models.ForeignKey(
        verbose_name='user',
        to=User,
        on_delete=models.CASCADE,
        related_name='refresh_tokens',
        null=True
    )
    # Token by itself
    refresh_token: str = models.CharField(
        verbose_name='token',
        max_length=229,
        null=True
    )
    # Datetime when token is expired
    expire_datetime: datetime.datetime = models.DateTimeField(
        verbose_name='expire datetime',
        default=timezone.now,
        null=True
    )
    # Finegerprint to upgrade security
    fingerprint: str = models.CharField(
        verbose_name='fingerprint',
        max_length=32,
        null=True
    )
    # Ip to upgrade security
    ip: str = models.CharField(
        verbose_name='ip',
        max_length=15,
        null=True
    )
    # Manager
    objects: RefreshTokenManager = RefreshTokenManager()

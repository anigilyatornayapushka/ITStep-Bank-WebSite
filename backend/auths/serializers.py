# DRF
from rest_framework import serializers

# Django
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth import (
    authenticate,
    login,
    get_user_model,
)
from django.utils import timezone

# Simple JWT
from rest_framework_simplejwt.tokens import RefreshToken

# Local
from .utils import generate_code
from .services.token_utils import add_token_to_db
from .services.user_utils import get_user_ip
from .validators import (
    is_email_confirmed,
    email_validation_error,
    gender_validation_error,
    password_validation_error,
    login_data_validation_error,
    user_code_validation,
    refresh_token_validation_error,
)
from .models import (
    AccountCode,
    TokenWhiteList,
)

# Third-party
from abstracts.mixins import AccessTokenMixin
from abstracts.serializers import CheckFieldsValidSerializer

# Python
import datetime


User: AbstractBaseUser = get_user_model()


class RegistrateUserSerializer(CheckFieldsValidSerializer,
                               serializers.ModelSerializer):
    """
    User serializer for registration.
    """

    email: str = serializers.CharField(max_length=60)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',
                  'password', 'password2', 'gender')

    def validate(self, attrs: dict) -> dict:
        """Validation of data."""
        email: str = attrs.get('email')
        gender: str = attrs.get('gender')
        password: str = attrs.get('password')
        password2: str = attrs.get('password2')

        # Check if email is valid
        email_validation_error(email=email,
                               raise_exception=True)

        # Chcek if passwords are valid
        password_validation_error(password1=password,
                                  password2=password2,
                                  raise_exception=True)

        # Check if genre is valid
        gender_validation_error(gender=gender, raise_exception=True)

        # Check if user is already confirmed
        status: str = is_email_confirmed(email=email, raise_exception=True)

        # Use it then in .save()
        self.status = status
        return attrs

    def save(self) -> None:
        """
        Save user with deactivation of account and hashing password.

        `signals.py`
    >>> ...
        u.set_password(password)
        ...
        """
        email: str = self.validated_data.get('email')
        first_name: str = self.validated_data.get('first_name')
        last_name: str = self.validated_data.get('last_name')
        password: str = self.validated_data.get('password')
        user: User | None = User.objects.get_object_or_none(email=email)

        if user:
            # If user is already created
            user.first_name = first_name
            user.last_name = last_name
            user.password = password
            user.set_password(password)
            user.password2 = user.password
            user.save()
        else:
            # If user registrated for the first time
            user: User = User.objects.create(**self.validated_data)

        # Use AccountCode.ACCOUNT_ACTIVATION to make code more readable
        code_type: int = AccountCode.ACCOUNT_ACTIVATION

        # Use AccountCode.CODE_LENGTH to make code scalable
        code_length: int = AccountCode.CODE_LENGTH

        # Create new account activation code
        AccountCode.objects.create(user=user, code=generate_code(code_length),
                                   code_type=code_type)

    def get_response(self) -> dict:
        """
        Return response to the view.
        """
        response: dict = {
            'data': 'Confirm your account. Code was sent on your email.'
        }
        return response


class LoginUserSerializer(CheckFieldsValidSerializer):
    """
    User serializer for log in.
    """

    email: str = serializers.CharField(max_length=60)
    password: str = serializers.CharField(max_length=128)

    def validate(self, attrs: dict) -> dict:
        """
        Validation of data.
        """
        email: str = attrs.get('email')
        password: str = attrs.get('password')
        user: User | None = authenticate(email=email,
                                         password=password)
        # Check if user allowed to log in
        login_data_validation_error(email=email,  password=password, user=user,
                                    raise_exception=True)

        # Set attribute .user to use it then in .save()
        self.user = user
        return attrs

    def save(self) -> None:
        """
        Generate refresh and access token or login(user) if it is admin.
        """
        user: User = self.user
        if user.is_admin:
            login(request=self.request, user=user)
            # Set attribute .is_admin to use it then in .get_response()
            self.is_admin = True
        else:
            self.is_admin = False

        # Generate token pair and create
        # attribute .refresh to use in then in .get_response()
        refresh: RefreshToken = RefreshToken.for_user(user)

        # Define some variables for refresh token
        ip: str = get_user_ip(request=self.request)
        fingerprint: str = self.request.COOKIES.get('fingerprint', '')

        # Add refresh token in database
        add_token_to_db(user=user, token=str(refresh), ip=ip,
                        fingerprint=fingerprint)

        # Set attribute .isrefresh to use it then in .get_response()
        self.refresh = refresh

    def get_response(self) -> dict:
        """
        Return response to the view.
        """
        # If user is admin, return link to admin panel
        if self.is_admin:
            response: dict = {
                'admin-url': 'http://'+self.request.get_host()+'/admin/'
            }
            response.update(response)

        # Response if user is not admin
        else:
            response: dict = {
                'refresh': str(self.refresh),
                'access': str(self.refresh.access_token)
            }

        return response


class ActivateAccountSerializer(CheckFieldsValidSerializer):
    """"
    Serializer for account activation view.
    """

    email: str = serializers.CharField(max_length=60)
    code: str = serializers.CharField(max_length=50)

    def validate(self, attrs: dict) -> dict:
        """
        Validation of data.
        """
        email: str = attrs.get('email')
        code: str = attrs.get('code')

        # Find user with this email
        user: User | None = User.objects.get_object_or_none(email=email)

        # Set .user attribute to use it then in .save()
        self.user = user

        # Check if there such code to the user
        code_type: int = AccountCode.ACCOUNT_ACTIVATION
        code: AccountCode = user_code_validation(user=user, code=code,
                                                 code_type=code_type,
                                                 raise_exception=True)
        # Delete used code
        code.datetime_expire = timezone.now()
        code.save(update_fields=('datetime_expire',))

        return attrs

    def save(self) -> None:
        """
        Make user `is_acitve = True` and save data.
        """
        self.user.is_active = True

        # Activate user's account
        self.user.save(update_fields=('is_active',))

    def get_response(self) -> dict:
        """
        Return response to the view.
        """
        response: dict = {
            'data': 'You confirmed your account successfully.'
        }
        return response


class ChangePasswordSerializer(CheckFieldsValidSerializer, AccessTokenMixin):
    """
    Serializer for user to reset password.
    """

    password: str = serializers.CharField()
    password2: str = serializers.CharField()

    def validate(self, attrs: dict) -> dict:
        """
        Validation of data.
        """
        password: str = attrs.get('password')
        password2: str = attrs.get('password2')

        # get_user() from AccessTokenMixin and
        # self.request from CommonPostMixin
        user, _ = self.get_user(request=self.request)

        # Set .user attribute to use it then in .save()
        self.user = user

        # Chcek if password is valid
        password_validation_error(password1=password, password2=password2,
                                  user=user, raise_exception=True)

        return attrs

    def save(self) -> None:
        """
        Save user's new password.
        """
        password: str = self.validated_data.get('password')

        # .user was setted in .validate()
        user: User = self.user

        # Set hashed password to user
        user.set_password(password)

        # Set hashed password2 to user
        user.password2 = user.password

        # Save data
        user.save(update_fields=('password', 'password2'))

    def get_response(self) -> dict:
        """
        Return response to the view.
        """
        response: dict = {
            'data': 'You reset your password successfully.'
        }
        return response


class ForgetPasswordSerializer(CheckFieldsValidSerializer):
    """
    Serializer for user to get reset password code.
    """

    email: str = serializers.CharField(max_length=60)

    def validate(self, attrs: str) -> dict:
        """
        Validation of data.
        """
        email: str = attrs.get('email')

        # Check if email is valid
        email_validation_error(email=email, find_user=True,
                               raise_exception=True)
        # Get user by email
        user: User = User.objects.get_object_or_none(email=email)

        # Set .user attribute to use it then in .save()
        self.user = user

        return attrs

    def save(self) -> None:
        """
        Save data.
        """
        user: User = self.user
        # AccountCode.PASSWORD_RESET to make code more readable
        code_type: int = AccountCode.PASSWORD_RESET

        # AccountCode.CODE_LENGTH to make code scalable
        code_length: int = AccountCode.CODE_LENGTH

        # Create new account password reset code
        AccountCode.objects.create(user=user, code_type=code_type,
                                   code=generate_code(code_length))

    def get_response(self) -> dict:
        """
        Return response to the view.
        """
        response: dict = {
            'data': 'Reset password code was sent on your email.'
        }
        return response


class ConfirmPasswordSerializer(CheckFieldsValidSerializer):
    """
    Confirm code to change user password.
    """

    code: str = serializers.CharField(max_length=AccountCode.CODE_LENGTH)
    email: str = serializers.CharField(max_length=60)
    password: str = serializers.CharField(max_length=128)
    password2: str = serializers.CharField(max_length=128)

    def validate(self, attrs: dict) -> dict:
        """
        Validation of data.
        """
        password: str = attrs.get('password')
        password2: str = attrs.get('password2')
        email: str = attrs.get('email')
        code: str = attrs.get('code')

        # Check if email is valid
        email_validation_error(email=email, find_user=True,
                               raise_exception=True)

        # Check if passwords are valid
        password_validation_error(password1=password, password2=password2,
                                  raise_exception=True)

        # Find user with this email
        user: User = User.objects.get_object_or_none(email=email)

        # Set .user attribute to use it then in .save()
        self.user = user
        code_type: int = AccountCode.PASSWORD_RESET

        # Check if code is valid
        code: AccountCode = user_code_validation(user=user, code=code,
                                                 code_type=code_type,
                                                 raise_exception=True)
        # Delete used code
        code.datetime_expire: datetime.datetime = timezone.now()
        code.save(update_fields=('datetime_expire',))

        return attrs

    def save(self) -> None:
        """
        Save data.
        """
        user: User = self.user
        password: str = self.validated_data.get('password')
        user.set_password(password)
        user.password2 = user.password
        user.save(update_fields=('password', 'password2'))

    def get_response(self) -> dict:
        """
        Return response to view.
        """
        response: dict = {
            'data': 'You changed password successfullyy'
        }
        return response


class RefreshTokenSerializer(CheckFieldsValidSerializer):
    """
    Serializer to refresh token.
    """

    refresh: str = serializers.CharField(max_length=229, min_length=229)

    def validate(self, attrs: dict) -> dict:
        """
        Data validation.
        """
        token: str = attrs.get('refresh')
        ip: str = get_user_ip(request=self.request)
        fingerprint: str = self.request.COOKIES.get('fingerprint', '')

        # Validate refresh token data
        refresh_token_validation_error(token=token, fingerprint=fingerprint,
                                       ip=ip, raise_exception=True)

        return attrs

    def save(self) -> None:
        """
        Save data.
        """
        refresh: str = self.validated_data.get('refresh')
        token: RefreshToken = RefreshToken(token=refresh)
        self.access_token = token.access_token

    def get_response(self) -> dict:
        """
        Return response to view.
        """
        response: dict = {
            'access': str(self.access_token)
        }
        return response


class LogoutSerializer(CheckFieldsValidSerializer, AccessTokenMixin):

    def validate(self, attrs: dict) -> dict:
        """
        Data validation.
        """
        # self.request from CommonPostMixin
        # self.get_user() from AccessTokenMixin
        user, _ = self.get_user(request=self.request)

        # Delete all user tokens
        TokenWhiteList.objects.filter(user=user).delete()

        return attrs

    def save(self) -> None:
        """
        Save data.
        """
        # Empty but defined because needed in CommonPostView
        pass

    def get_response(self) -> dict:
        """
        Return response to view.
        """
        response: dict = {
            'data': 'You logged out successfully.'
        }
        return response


class UserSerializer(CheckFieldsValidSerializer, AccessTokenMixin):
    """
    Serializer for user.
    """

    first_name: str = serializers.CharField()
    last_name: str = serializers.CharField()
    email: str = serializers.CharField()
    gender: str = serializers.CharField()

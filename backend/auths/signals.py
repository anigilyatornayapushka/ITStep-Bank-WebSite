# Django
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import (
    pre_save,
    post_save,
)

# Local
from .models import AccountCode
from .tasks import (
    send_account_activation_email,
    send_reset_password_email,
)

# Python
import typing as t


User: AbstractBaseUser = get_user_model()


@receiver(signal=post_save, sender=User)
def user_post_save(instance: User, created: bool, **kwargs: t.Any) -> None:
    if created:
        # Hash user password after creation
        instance.set_password(instance.password)
        instance.password2 = instance.password
        instance.save(update_fields=('password', 'password2'))


@receiver(signal=pre_save, sender=AccountCode)
def accountcode_pre_save(instance: AccountCode, **kwargs: t.Any) -> None:
    """
    Send account activation code on user's email after registration.
    """
    user: User = instance.user
    if instance.code_type == AccountCode.ACCOUNT_ACTIVATION:
        send_account_activation_email(user.email, user.fullname, instance.code)
    elif instance.code_type == AccountCode.PASSWORD_RESET:
        send_reset_password_email(user.email, user.fullname, instance.code)

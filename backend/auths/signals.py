# Django
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import (
    pre_save,
    post_save,
)

# Python
import typing as t

# Local
from .models import AccountCode
from .utils import TextEmailSender


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
        sender: TextEmailSender = TextEmailSender(
            send_to=user.email,
            subject='Account activation',
            message=(
                'Dear %s,\n\n'
                'We are delighted to welcome you and inform you of '
                'your successful registration. As part of\nthe registration '
                'process, we have generated a unique activation code for you.'
                '\nPlease find your code below:\n\nActivation Code: %s\n\n'
                'To complete the registration, please click on the\n'
                'following link: http://127.0.0.1:8000/account/activation/%s/'
                '\n\nOnce you click on the link, you will be redirected to'
                'our website, where you can enter the\nactivation code and'
                'proceed with the next steps.\n\nIf you have any questions'
                'or need assistance, please feel free to reach out to our'
                'support\nteam. We are here to help you.\n\nThank you once'
                'again for choosing our platform.\n\nWe look forward to '
                'your active participation.\n\nBest regards,\n\nItStepBank'
            ) % (user.fullname, instance.code, user.email)
        )
        sender.send_email()
    elif instance.code_type == AccountCode.PASSWORD_RESET:
        sender: TextEmailSender = TextEmailSender(
            send_to=user.email,
            subject='Password reset',
            message=(
                'Hello, %s.'
                'Enter this code on the site to reset a password:\n'
                '%s\n'
                'If it wasn\'t you, just ignore the message'
                % (user.fullname, instance.code)
            )
        )
        sender.send_email()

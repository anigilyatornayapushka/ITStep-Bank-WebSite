# Celery
from celery import shared_task

# Local
from .utils import TextEmailSender


@shared_task
def send_account_activation_email(email: str, fullname: str, code: str):
    sender: TextEmailSender = TextEmailSender(
        send_to=email,
        subject='Account activation',
        message=(
            'Hello, %s.'
            'Enter this code on the site to confirm registration:\n'
            '%s\n'
            'If it wasn\'t you, just ignore the message'
            % (fullname, code)
        )
    )
    sender.send_email()


@shared_task
def send_reset_password_email(email: str, fullname: str, code: str):
    sender: TextEmailSender = TextEmailSender(
        send_to=email,
        subject='Password reset',
        message=(
            'Hello, %s.'
            'Enter this code on the site to reset a password:\n'
            '%s\n'
            'If it wasn\'t you, just ignore the message'
            % (fullname, code)
        )
    )
    sender.send_email()

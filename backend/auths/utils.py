# Python
import random
from abc import (
    ABCMeta,
    abstractmethod,
)

# Django
from django.core.mail import send_mail
from django.template.loader import render_to_string


# alphabet of generated code
alpha: str = 'qwertyuiopasdfghjklzxcvbnm1234567890#!?/*^$@'


def generate_code(length: int) -> str:
    """
    Generate a random code of a certain length.

    Code contains letters and numbers.
    """
    code: str = ''
    for _ in range(length):
        code = code + random.choice(alpha)
    return code


class BaseEmailSender(metaclass=ABCMeta):
    """
    Interface for classes that implement the method

    of sending a mail to the email in different ways.
    """

    def __init__(self, send_to: str, subject: str) -> None:
        # The person to whom the letter is sent
        self.send_to = send_to
        # Subject of the message
        self.subject = subject

    @abstractmethod
    def send_email(self) -> None:
        pass


class TextEmailSender(BaseEmailSender):
    """
    Send message on the email as text.
    """

    def __init__(self, send_to: str, subject: str, message: str) -> None:
        # Text message to user
        self.message = message
        super().__init__(send_to=send_to, subject=subject)

    def send_email(self) -> None:
        send_mail(
            subject=self.subject,
            message=self.message,
            from_email=None,
            recipient_list=[self.send_to],
            fail_silently=True
        )


class HTMLEmailSender(TextEmailSender):
    """
    Send message on the email as html document.
    """

    def __init__(self, send_to: str, subject: str,
                 message: str, template_name: str,
                 context: dict) -> None:
        # Template name, that will be converted to the message to user
        self.message = message
        self.template_name = template_name
        self.context = context
        super().__init__(send_to=send_to, subject=subject)

    def send_email(self) -> None:
        html_message: str = render_to_string(template_name=self.template_name,
                                             context=self.context)
        send_mail(
            subject=self.subject,
            message=self.message,
            from_email=None,
            recipient_list=[self.send_to],
            fail_silently=True,
            html_message=html_message
        )

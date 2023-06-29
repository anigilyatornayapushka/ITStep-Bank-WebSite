# Django
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

# Python
import random
import hashlib
import abc


# alphabet of generated code
alpha: str = '1234567890'


def generate_code(length: int) -> str:
    """
    Generate a random code of a certain length.

    Code contains letters and numbers.
    """
    code: str = ''
    for _ in range(length):
        code = code + random.choice(alpha)
    return code


class BaseEmailSender(metaclass=abc.ABCMeta):
    """
    Interface for classes that implement the method

    of sending a mail to the email in different ways.
    """

    def __init__(self, send_to: str, subject: str, message: str) -> None:
        # The person to whom the letter is sent
        self.send_to = send_to
        # Subject of the message
        self.subject = subject
        # Message itself
        self.message = message

    @abc.abstractmethod
    def send_email(self) -> None:
        pass


class TextEmailSender(BaseEmailSender):
    """
    Send message on the email as text.
    """

    def send_email(self) -> None:
        # Send message on the inbox
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

    def send_html_email(self, template_name: str, context: dict) -> None:
        # Generate HTML message
        html_message: str = render_to_string(template_name=template_name,
                                             context=context)

        # Send message on the inbox
        send_mail(
            subject=self.subject,
            message=self.message,
            from_email=None,
            recipient_list=[self.send_to],
            fail_silently=True,
            html_message=html_message
        )


class BaseHasher(metaclass=abc.ABCMeta):
    """
    Base hasher.
    """

    @abc.abstractmethod
    def hash(self, string: str) -> str:
        """
        Hash string.
        """
        pass


class Sha256Hasher(BaseHasher):
    """
    Hasher using sha256.
    """

    def hash(self, string: str) -> str:
        # Create salt
        salt = settings.SECRET_KEY.encode('utf-8')

        # Hash string
        hash_object = hashlib.sha256()
        token_with_salt = string.encode('utf-8') + salt
        hash_object.update(token_with_salt)
        hash_result = hash_object.hexdigest()

        return hash_result

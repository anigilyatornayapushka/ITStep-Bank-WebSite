# Django
from django.core.mail import send_mail
from django.template.loader import render_to_string

# Python
import abc


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

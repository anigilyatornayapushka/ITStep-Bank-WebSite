# Django
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import (
    pre_save,
    post_save,
)

# RabbitMQ
import pika

# Python
import json
import typing as t
import decouple

# Local
from .models import AccountCode


User: AbstractBaseUser = get_user_model()


class RabbitMQConnection:
    """
    Connection with rabbitMQ server and send messages.
    """

    queue_name: str = 'email_to_send'
    exchange_name: str = 'email_to_send_exchange'

    @property
    def credentials(self) -> pika.PlainCredentials:
        # Get creditionals from environment
        username: str = decouple.config('RABBITMQ_USERNAME', cast=str)
        password: str = decouple.config('RABBITMQ_PASSWORD', cast=str)

        # Create PlainCreditionals for pika
        credentials = pika.PlainCredentials(username=username,
                                            password=password)
        return credentials

    def __enter__(self) -> 'RabbitMQConnection':
        """
        Open connection.
        """
        # Define parameters of connection
        params: pika.ConnectionParameters =\
            pika.ConnectionParameters(host='127.0.0.1', port=5672,
                                      credentials=self.credentials)

        # Create connection
        connection: pika.BlockingConnection =\
            pika.BlockingConnection(parameters=params)
        self.connection = connection

        # Get channel
        channel = connection.channel()
        self.channel = channel

        # Declare queue
        channel.queue_declare(queue=self.queue_name, durable=True)

        return self

    def send_message(self, message: str, subject: str, send_to: str) -> None:
        """
        Send message to the queue.
        """
        # Make dictionary to send
        message_dict: dict = {
            'to': send_to,
            'message': message,
            'subject': subject
        }

        # Convert to the string format
        message_text: str = json.dumps(obj=message_dict)

        # Send message
        self.channel.basic_publish(exchange=self.exchange_name,
                                   routing_key='',
                                   body=message_text)

    def __exit__(self, *args: t.Any) -> None:
        """
        Close connection.
        """
        self.connection.close()


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
    # Open connection with rabbitMQ server
    with RabbitMQConnection() as connection:

        # User
        user: User = instance.user

        if instance.code_type == AccountCode.ACCOUNT_ACTIVATION:
            # Subject of mail
            subject: str = 'Account activation'

            # Body of mail
            message: str = (
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

        elif instance.code_type == AccountCode.PASSWORD_RESET:
            # Subject of mail
            subject: str = 'Password reset'

            # Body of mail
            message: str = (
                'Hello, %s.'
                'Enter this code on the site to reset a password:\n'
                '%s\n'
                'If it wasn\'t you, just ignore the message'
                % (user.fullname, instance.code)
            )

        # Send message
        connection.send_message(
            send_to=user.email,
            subject=subject,
            message=message
        )

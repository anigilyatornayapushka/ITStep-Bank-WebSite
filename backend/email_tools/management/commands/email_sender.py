# Django
from django.core.management.base import BaseCommand

# RabbitMQ
import pika

# Python
import typing as t
import decouple
import json

# Third-party
from auths.utils import TextEmailSender


class Command(BaseCommand):
    """
    Get messages from rabbitMQ queue and send mail.
    """

    def _callback(self, channel, method, properties, body) -> None:
        # Decode message
        string_body: str = body.decode()

        # Convert message to dictionary
        dict_body: dict = json.loads(string_body)

        # Get arguments
        send_to: str = dict_body.get('to')
        subject: str = dict_body.get('subject')
        message: str = dict_body.get('message')

        # Send email
        sender: TextEmailSender = TextEmailSender(
            send_to=send_to,
            subject=subject,
            message=message
        )
        sender.send_email()
        print('[i] %s | %s' % (subject, send_to))

    def start_consuming(self, *args: t.Any, **kwargs: t.Any) -> None:
        """Consuming of messages."""
        print('Start consuming...')

        # Name of queue
        queue_name: str = 'email_to_send'

        # Creditionals
        username: str = decouple.config('RABBITMQ_USERNAME', cast=str)
        password: str = decouple.config('RABBITMQ_PASSWORD', cast=str)
        credentials = pika.PlainCredentials(username=username,
                                            password=password)

        # Define parameters of connection
        params: pika.ConnectionParameters =\
              pika.ConnectionParameters(host='127.0.0.1',
                                        port=5672,
                                        credentials=credentials)

        # Create connection
        connection: pika.BlockingConnection =\
            pika.BlockingConnection(parameters=params)
        self.connection = connection

        # Get channel
        channel = connection.channel()

        # Declare queue
        channel.queue_declare(queue=queue_name, durable=True)

        # Create consumer
        channel.basic_consume(queue=queue_name,
                            on_message_callback=self._callback,
                            auto_ack=True)

        # Enter the infinite loop to process messages
        while True:
            try:
                channel.start_consuming()
            except KeyboardInterrupt:
                self.connection.close()
                print('Stop consuming...')
                break

    def handle(self, *args: t.Any, **kwargs: t.Any):
        """
        Handle command.
        """
        self.start_consuming(*args, **kwargs)

# Local
from ..models import (
    Card,
    Transaction,
)
from ..caches import RedisConnector

# DRF
from rest_framework import serializers

# Django
from django.db.models import Sum
from django.db import transaction
from django.conf import settings

# Python
import typing as t
import requests
from decimal import Decimal


def check_balance(number: str, currency: str) -> float:
    """
    Count balance on card by transactions.
    """
    # Get card of user
    card: Card = Card.objects.get_object_or_none(number=number)

    # Count money received by card
    received: float = Transaction.objects.filter(
        card_receiver=card, currency=currency
    ).aggregate(total=Sum('balance')).get('total') or 0

    # Count money spent by card
    spent: float = Transaction.objects.filter(
        card_sender=card, currency=currency
    ).aggregate(total=Sum('balance')).get('total') or 0

    # Count actual balance of the card
    return received - spent


def create_transaction(**kwargs: t.Any) -> Transaction:
    """
    Create transaction object. Kwargs must contain

    number1 (sender), number2 (receiver), balance, currency.

    Optional: is_convertation.
    """
    # Define card sender
    card_sender_number: str = kwargs.get('number1')
    if card_sender_number is None:
        sender: None = None
    else:
        sender: Card = Card.objects.get(number=card_sender_number)

    # Define card receiver
    card_receiver_number: str = kwargs.get('number2')
    if card_receiver_number is None:
        receiver: None = None
    else:
        receiver: Card = Card.objects.get(number=card_receiver_number)

    # Define other fields
    balance: float = kwargs.get('balance')
    currency: str = kwargs.get('currency')
    is_convertation: bool = kwargs.get('is_convertation', False)

    # Create transaction
    transaction: Transaction =\
        Transaction.objects.create(card_receiver=receiver, balance=balance,
                                   card_sender=sender, currency=currency,
                                   is_convertation=is_convertation)

    return transaction


def get_the_exchange_rate(currency1: str, currency2: str) -> float:
    """
    Get the current exchange rate.
    """

    # Use redis connector to conect with redis
    with RedisConnector(db=0) as server:

        # Define key for the user request
        key: str = currency1 + currency2

        # If already in cache
        if result := server.get(key):
            return result

        # Define request options
        url: str = settings.EXCHANGE_RATES_URL + currency1

        # Do request to the exchange rates api
        response: requests.Response = requests.get(url=url)

        # Get data
        data: dict = response.json()

        if data.get('result') == 'error':
            err: list = ['Something went wrong.']
            raise serializers.ValidationError({'error': err})

        # Exchange
        exchange: float = data.get('conversion_rates').get(currency2)
        exchange: Decimal = Decimal(str(exchange))

        # Add result to the redis
        server.set(key=key, value=exchange, eta=60*5)

        return exchange


@transaction.atomic
def do_currency_convertation(**kwargs: t.Any) -> None:
    """
    Do currency convertation. Kwargs must contain

    number, currency1, currency2, balance.
    """
    # Defina variables
    number: str = kwargs.get('number')
    currency1: str = kwargs.get('currency1')
    currency2: str = kwargs.get('currency2')
    balance: float = kwargs.get('balance')

    # Get exchange
    exchange: Decimal = get_the_exchange_rate(currency1=currency1,
                                              currency2=currency2)

    # Do transactions
    create_transaction(number1=number, number2=None, balance=balance,
                       currency=currency1, is_convertation=True)
    create_transaction(number1=None, number2=number, balance=balance*exchange,
                       currency=currency2, is_convertation=True)

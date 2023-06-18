# DRF
from rest_framework import serializers

# Django
from django.conf import settings

# Local
from .models import (
    Card,
    Transaction,
)
from .validators import (
    do_transaction_validation_error,
    currency_validation_error,
    balance_validation_error,
)
from .services.transaction_utils import check_balance

# Third-party
from abstracts.serializers import CheckFieldsValidSerializer


class ShowCardsSerializer(CheckFieldsValidSerializer):
    """
    Serializer for create card view.
    """

    number: str = serializers.CharField(max_length=16, min_length=16)
    cvv: str = serializers.CharField(max_length=3, min_length=3)
    balance: float = serializers.SerializerMethodField(
        method_name='get_balance'
    )

    def get_balance(self, obj: Card) -> float:
        """
        Get balance on all cards in all currencies.
        """
        # Iter all user balances
        all_balance: dict = {}
        for currency in settings.ALLOWED_CURRENCY:

            # Check user balance in all alowed currencies
            all_balance[currency] = check_balance(number=obj.number,
                                                  currency=currency)
        return all_balance


class ShowTransactionsSerializer(CheckFieldsValidSerializer):
    """
    Serializer to show all transactions.
    """

    sender: str = serializers.SerializerMethodField(
        method_name='get_sender'
    )
    receiver: str = serializers.SerializerMethodField(
        method_name='get_receiver'
    )
    currency: str = serializers.CharField(max_length=3, min_length=3)
    balance: float = serializers.DecimalField(max_digits=8, decimal_places=2)

    def get_sender(self, obj: Transaction) -> str:
        """
        Get number of card | None.
        """
        if card := obj.card_sender:
            return card.number

    def get_receiver(self, obj: Transaction) -> str:
        """
        Get number of card | None.
        """
        if card := obj.card_receiver:
            return card.number


class DoTransactionSerializer(CheckFieldsValidSerializer):
    """
    Serializer to do transactions between users.
    """

    balance: float = serializers.DecimalField(max_digits=8, decimal_places=2)
    currency: str = serializers.CharField(max_length=3, min_length=3)
    number1: str = serializers.CharField(max_length=16, min_length=16)
    number2: str = serializers.CharField(max_length=16, min_length=16)

    def validate(self, attrs: dict) -> dict:
        """
        Data validation.
        """
        balance: float = attrs.get('balance')
        currency: str = attrs.get('currency')
        number1: str = attrs.get('number1')
        number2: str = attrs.get('number2')

        # self.user has been set inside the View
        # Validate card numbers
        do_transaction_validation_error(user=self.user, number1=number1,
                                        number2=number2, raise_exception=True)

        # Validate currency
        currency_validation_error(currency1=currency, raise_exception=True)

        # Validate balance
        balance_validation_error(balance=balance, number=number1,
                                 currency=currency, raise_exception=True)

        return attrs


class ConvertCurrencySerializer(CheckFieldsValidSerializer):
    """
    Serializer to check, if currency convertation is available.
    """

    number: str = serializers.CharField(max_length=16, min_length=16)
    balance: float = serializers.DecimalField(max_digits=8, decimal_places=2)
    currency1: str = serializers.CharField(max_length=3, min_length=3)
    currency2: str = serializers.CharField(max_length=3, min_length=3)

    def validate(self, attrs: dict) -> dict:
        """
        Data validation.
        """
        # Define variables
        balance: float = attrs.get('balance')
        number: str = attrs.get('number')
        currency1: str = attrs.get('currency1')
        currency2: str = attrs.get('currency2')

        # Check if currency that user want to get is valid
        currency_validation_error(currency1=currency1, currency2=currency2,
                                  raise_exception=True)

        # Check if data to do transaction is valid
        do_transaction_validation_error(user=self.user, number1=number,
                                        number2=None, raise_exception=True)

        # Validate if user can convert currency
        balance_validation_error(balance=balance, number=number,
                                 currency=currency1, raise_exception=True)

        # If currencies are the same
        if currency1 == currency2:

            # Raise exception
            err: dict = {
                'currency1': ['You can\'t change currency to itself.'],
                'currency2': ['You can\'t change currency to itself.']
            }
            raise serializers.ValidationError(err)

        return attrs


class ReplenishmentSerializer(CheckFieldsValidSerializer):
    """
    Serializer for user to replenish balance.
    """

    number: str = serializers.CharField(max_length=16, min_length=16)
    balance: float = serializers.DecimalField(max_digits=8, decimal_places=2)
    currency: str = serializers.CharField(max_length=3)

    def validate(self, attrs: dict) -> dict:
        """
        Data validation.
        """
        number: str = attrs.get('number')
        balance: str = attrs.get('balance')
        currency: str = attrs.get('currency')

        # Check if currency that user want to get is valid
        currency_validation_error(currency1=currency, raise_exception=True)

        # Check if data to do transaction is valid
        do_transaction_validation_error(user=self.user, number1=number,
                                        raise_exception=True)

        # Validate if user can replenish currency
        balance_validation_error(balance=balance, number=number,
                                 check_card_balance=False, currency=currency,
                                 raise_exception=True)

        # Add number2 key to then recognize the card number
        # as a receiver in create_transaction function
        attrs['number2'] = number

        return attrs

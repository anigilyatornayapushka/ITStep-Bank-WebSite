# Django
from django.core.exceptions import ValidationError
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth import get_user_model
from django.conf import settings

# Local
from .models import Card
from .services.transaction_utils import check_balance

# Python
import re


User: AbstractBaseUser = get_user_model()


def currency_validation_error(currency1: str, currency2: str = None,
                              raise_exception: bool = False
                              ) -> dict | None:
    """
    Validate currency. Check if it is allowed in settings.
    """
    # Error, that will be returned or raised
    error: dict = {'currency1': [], 'currency2': []}

    # Check if currency allowed
    if currency1 not in settings.ALLOWED_CURRENCY:

        # Add error to the errors dict
        err: str = 'Currency is not allowed.'
        error['currency1'].append(err)

    # Check if currency allowed
    if currency2 and currency2 not in settings.ALLOWED_CURRENCY:

        # Add error to the errors dict
        err: str = 'Currency is not allowed.'
        error['currency2'].append(err)

    # Check if currency length is valid
    if len(currency1) != 3:

        # Add error to the errors dict
        err: str = 'Currency must be 3 letters length.'
        error['currency1'].append(err)

    # Check if user tries to convert currency to itself
    if currency1 == currency2:

        # Add error to the errors dict
        err: str = 'You can\'t convert currency to itself'
        error['currency1'].append(err)

    # Check if there any errors
    have_errors: bool = error.get('currency1') or error.get('currency2')

    # If there any errors and flag raise_exception is on, raise exception
    if have_errors and raise_exception is True:
        raise ValidationError(error)

    return error if have_errors else None


def do_transaction_validation_error(user: User, number1: str,
                                    number2: str = None,
                                    raise_exception: bool = False
                                    ) -> dict | None:
    """
    Check if data to do transaction is valid.
    """
    # Error, that will be returned or raised
    error: dict = {
        'number1': [],
        'number2': []
    }

    pattern: str = r'^4400[123]\d{11}$'

    # Check if card number match the pattern
    if not re.match(string=number1, pattern=pattern):

        # Add error to the errors dict
        err: list = ['Card number doesn\'t match pattern']
        error['number1'].append(err)

    # Check if card number match the pattern
    if number2 and not re.match(string=number2, pattern=pattern):

        # Add error to the errors dict
        err: list = ['Card number doesn\'t match pattern']
        error['number2'].append(err)

    # If user tries to transferm money to itself
    if number2 and number1 == number2:

        # Add error to the errors dict
        err: str = 'You cannot transfer money to the same card you use'
        error['number1'].append(err)

    # Check if user card number is valid
    if not user.cards.filter(number=number1).exists():

        # Add error to the errors dict
        err: str = 'You have not card with number %s.' % number1
        error['number1'].append(err)

    # Check if receiver card number is valid
    if number2 and not Card.objects.filter(number=number2).exists():

        # Add error to the errors dict
        err: str = 'You cannot transfer money to a non-existent card.'
        error['number2'].append(err)

    # Check if there are any errors
    have_errors: bool = error.get('number1') or error.get('number2')

    # If there any errors and flag raise_exception is on, raise exception
    if have_errors and raise_exception is True:
        raise ValidationError(error)

    return error if have_errors else None


def balance_validation_error(balance: float, number: str, currency: str,
                             check_card_balance: bool = True,
                             raise_exception: bool = False) -> dict | None:
    """
    Validate balance in transaction.
    """
    # Error, that will be returned or raised
    error: dict = {'balance': []}

    # If transfer balance if valid
    if balance < 1:

        # Add error to the errors dict
        err: str = 'You must transfer at least 1 currency unit.'
        error['balance'].append(err)

    # If currency is valid
    else:

        # Get user actual balance
        card_balance: float = check_balance(number=number, currency=currency)

        # Check if user actual balance enough to do payment
        if check_card_balance is True and card_balance < balance:

            # Add error to the errors dict
            err: str = 'You have not enough money to do a transaction.'
            error['balance'].append(err)

    # Check if there are any errors
    have_errors: bool = error.get('balance')

    # If there any errors and flag raise_exception is on, raise exception
    if have_errors and raise_exception is True:
        raise ValidationError(error)

    return error if have_errors else None

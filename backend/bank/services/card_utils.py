# Django
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth import get_user_model

# Python
import random

# Local
from ..models import Card


User: AbstractBaseUser = get_user_model()


class CardGenerator:
    """
    Generate a new valid card.
    """

    def __init__(self, user: User) -> None:
        self.user = user

    def _generate_number(self) -> str:
        """
        Generate unique number for card.
        """
        # Generates code following a template
        number: str = '{0}{1}{2}'.format(
            4400,
            self.user.cards.count()+1,
            ''.join(random.choices('0123456789', k=11))
        )

        # Check if such number already exists
        if Card.objects.filter(number=number).exists():

            # Generate number again
            return self._generate_number()

        return number

    def _generate_cvv(self) -> str:
        """
        Generate CVV for card.
        """
        # Generate random cvv
        cvv: int = random.randrange(100, 1000)

        return str(cvv)

    def generate(self) -> Card:
        """
        Create new card and fill data.
        """
        # Create instance of card
        new_card: Card = Card()

        # Generate new unique card number
        new_card.number = self._generate_number()

        # Generate CVV
        new_card.cvv = self._generate_cvv()

        # Assign the owner
        new_card.user = self.user

        # Authenticate the card
        new_card.is_active = True

        # Save data of card in DB
        new_card.save()

        return new_card

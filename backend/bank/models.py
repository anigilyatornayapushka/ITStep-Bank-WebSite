# Django
from django.db import models
from django.db.models.query import QuerySet
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.validators import (
    MinLengthValidator,
    MinValueValidator,
    MaxValueValidator,
)

# Third-party
from abstracts.models import (
    AbstractModel,
    AbstractManager,
)


User: AbstractBaseUser = get_user_model()


class CardManager(AbstractManager):
    """
    Manager for card model.
    """

    pass


class Card(AbstractModel):
    """
    Card model.
    """

    # Maximmum cards per user
    MAX_CARD_LIMIT: int = 3
    # Card number pattern 4400-TNNN-NNNN-NNNN
    # 4400 - required
    # T - number of cards a user has
    # N - random number from 0 to 9
    number: str = models.CharField(
        verbose_name='number',
        max_length=16,
        validators=(
            MinLengthValidator(16),
        ),
        unique=True
    )
    # CVV code of number
    cvv: str = models.CharField(
        verbose_name='CVV',
        max_length=3,
        validators=(
            MinLengthValidator(3),
        )
    )
    # Owner of the card
    user: User = models.ForeignKey(
        verbose_name='owner',
        to=User,
        on_delete=models.PROTECT,
        related_name='cards'
    )
    # Manager
    objects: CardManager = CardManager()

    def __repr__(self) -> str:
        return self.number

    class Meta:
        ordering = (
            'user',
            'datetime_created',
        )
        verbose_name = 'card'
        verbose_name_plural = 'cards'


class TransactionManager(AbstractManager):
    """
    Manager for transaction model.
    """

    def get_for_user(self, user: User, filter: str) -> QuerySet['Transaction']:
        """
        Get all transactions for user cards

        using filter (received | spent | converted)
        """
        # Type annotation of queryset
        queryset: QuerySet[Transaction]

        # Define user cards to use it then
        cards: QuerySet[Card] = user.cards.all()

        # If user want to see only received money
        if filter == 'received':
            queryset = Transaction.objects.filter(
                card_receiver__in=cards,
                is_convertation=False
            ).select_related('card_sender', 'card_receiver')

        # If user want to see only spent money
        elif filter == 'spent':
            queryset = Transaction.objects.filter(
                card_sender__in=cards,
                is_convertation=False
            ).select_related('card_sender', 'card_receiver')

        # If user want to see only converted money
        elif filter == 'converted':
            queryset = Transaction.objects.filter(
                is_convertation=True
            ).select_related('card_sender', 'card_receiver')

        # If user want to see all transactions all filter is not valid
        else:
            queryset = Transaction.objects.filter(
                models.Q(card_receiver__in=cards) |
                models.Q(card_sender__in=cards)
            ).select_related('card_sender', 'card_receiver')

        return queryset


class Transaction(AbstractModel):
    """
    Transaction between cards.
    """
    # Allowed currency to keep on card
    ALLOWED_CURRENCY: tuple = (
        (currency, currency)
        for currency
        in settings.ALLOWED_CURRENCY
    )
    # Card sender of money
    card_sender: Card = models.ForeignKey(
        verbose_name='card sender',
        to=Card,
        on_delete=models.PROTECT,
        related_name='transactions_sended',
        blank=True,
        null=True
    )
    # Card receiver of money
    card_receiver: Card = models.ForeignKey(
        verbose_name='card receiver',
        to=Card,
        on_delete=models.PROTECT,
        related_name='transactions_received',
        blank=True,
        null=True
    )
    # Currency of transfered money
    currency: str = models.CharField(
        verbose_name='currency',
        max_length=3,
        validators=(
            MinLengthValidator(3),
        ),
        choices=ALLOWED_CURRENCY,
        null=True
    )
    # Transfered money
    balance: float = models.DecimalField(
        verbose_name='transfer amount',
        max_digits=8,
        decimal_places=2,
        validators=(
            MinValueValidator(100),
            MaxValueValidator(300_000),
        )
    )
    # Is convertation of currency or other
    is_convertation: bool = models.BooleanField(
        verbose_name='is convertation',
        default=False
    )
    # Manager
    objects: TransactionManager = TransactionManager()

    def __repr__(self) -> str:
        return '[%s] -> [%s]' % (self.card_sender.number,
                                 self.card_receiver.number)

    class Meta:
        ordering = (
            'id',
        )
        verbose_name = 'transaction'
        verbose_name_plural = 'transactions'

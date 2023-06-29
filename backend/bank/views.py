# Django
from django.contrib.auth.base_user import AbstractBaseUser
from django.db.models.query import QuerySet
from django.contrib.auth import get_user_model

# DRF
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

# Third-party
from abstracts.mixins import AccessTokenMixin

# Local
from .serializers import (
    ShowCardsSerializer,
    ShowTransactionsSerializer,
    DoTransactionSerializer,
    ConvertCurrencySerializer,
    BalanceSerializer,
)
from .models import (
    Card,
    Transaction,
)
from .services.card_utils import CardGenerator
from .services.transaction_utils import (
    MockTransfer,
    create_transaction,
    do_currency_convertation,
)
from .paginataion import BasePaginator


User: AbstractBaseUser = get_user_model()


class ShowCardsView(APIView, AccessTokenMixin):
    """
    Show all user cards.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class: ShowCardsSerializer = ShowCardsSerializer

    def get(self, request: Request) -> Response:
        """
        GET request.
        """
        # Get user by access token
        user = self.get_user(request=request)

        # Find all user cards
        card_queryset: QuerySet[Card] = user.cards

        # Serialization of data
        serializer = self.serializer_class(instance=card_queryset, many=True)

        # Return data
        return Response(data=serializer.data, status=200)


class ShowTransactionsView(APIView, AccessTokenMixin):
    """
    Show all user transactions.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class: ShowTransactionsSerializer = ShowTransactionsSerializer
    pagination_class: BasePaginator = BasePaginator

    def get(self, request: Request) -> Response:
        """
        GET request.
        """
        # filter variable to filer transactions queryset then
        filter: str = request.data.get('filter', '')

        # Pagination class instance
        paginator = self.pagination_class()

        # Get user by access token
        user = self.get_user(request=request)

        # Queryset of all user transactions. Filter if it is valid
        queryset: QuerySet[Transaction] = \
            Transaction.objects.get_for_user(user=user, filter=filter)

        # Get paginated queryset
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        # Serializer queryset
        serializer = self.serializer_class(instance=paginated_queryset,
                                           many=True)

        # Return paginated data
        response: dict = paginator.get_paginated_response(serializer.data)
        return Response(data=response, status=200)


class CreateCardView(APIView, AccessTokenMixin):
    """
    Create card view.
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request: Request) -> Response:
        """
        POST request.
        """
        # Get user using JWT access token
        user = self.get_user(request=request)

        # Chek is user can create new card
        if user.cards.count() >= Card.MAX_CARD_LIMIT:

            # If not return an error message
            err: dict = {
                'card': ['You can only create 3 cards.']
            }
            return Response(data=err, status=400)

        # Create CardGenerator instance and generate new card
        generator: CardGenerator = CardGenerator(user=user)
        card: Card = generator.generate()

        # Return success message
        data: dict = {
            'data': 'Card %s generated successfully.' % card.number
        }
        return Response(data=data, status=201)


class DoTransactionView(APIView, AccessTokenMixin):
    """
    Do transaction view.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class: DoTransactionSerializer = DoTransactionSerializer

    def post(self, request: Request) -> Response:
        """
        POST request.
        """
        # Serialization of data
        serializer = self.serializer_class(data=request.data)

        # Get user by access token
        user = self.get_user(request=request)

        # Define .user attribute to use it then in validation
        serializer.user = user

        # Validation
        serializer.is_valid(raise_exception=True)

        # Create transaction
        create_transaction(**serializer.validated_data)

        # Return success message
        response: dict = {
            'data': 'Transaction was successful.'
        }
        return Response(data=response, status=200)


class ConvertCurrencyView(APIView, AccessTokenMixin):
    """
    View to convert currency.
    """

    permission_classes: tuple = (IsAuthenticated,)
    serializer_class: ConvertCurrencySerializer = ConvertCurrencySerializer

    def post(self, request: Request) -> Response:
        """
        POST request.
        """
        # Get user by access token
        user = self.get_user(request=request)

        # Validate data
        serializer = self.serializer_class(data=request.data)

        # Set .user attribute to use it then in validation
        serializer.user = user

        # Validate data
        serializer.is_valid(raise_exception=True)

        # Convert currency
        do_currency_convertation(**serializer.validated_data)

        # Return success response
        response: dict = {
            'data': 'Convertation completed successfully.'
        }
        return Response(data=response, status=200)


class BalanceReplenishmentView(APIView, AccessTokenMixin):
    """
    View for user to replenish balance.
    """

    permission_classes: tuple = (IsAuthenticated,)
    serializer_class: BalanceSerializer = BalanceSerializer

    def post(self, request: Request) -> Response:
        """
        POST request.
        """
        # Get user by access token
        user = self.get_user(request=request)

        # Serializer data
        serializer = self.serializer_class(data=request.data)

        # Set .user attribute to use it then in validation
        serializer.user = user

        # Validate data
        serializer.is_valid(raise_exception=True)

        # Create transfer and put money from real on virtual card
        transfer: MockTransfer = MockTransfer()

        transfer.from_real_to_virtual(**serializer.validated_data)

        # Return response
        response: dict = {
            'data': 'Balance was replenished successfully.'
        }
        return Response(data=response, status=200)


class BalanceWithdrawView(APIView, AccessTokenMixin):
    """
    View for user to withdraw balance.
    """

    permission_classes: tuple = (IsAuthenticated,)
    serializer_class: BalanceSerializer = BalanceSerializer

    def post(self, request: Request) -> Response:
        """
        POST request.
        """
        # Get user by access token
        user = self.get_user(request=request)

        # Serializer data
        serializer = self.serializer_class(data=request.data)

        # Set .user attribute to use it then in validation
        serializer.user = user

        # Validate data
        serializer.is_valid(raise_exception=True)

        # Create transfer and put money from real on virtual card
        transfer: MockTransfer = MockTransfer()

        transfer.from_virtual_to_real(**serializer.validated_data)

        # Return response
        response: dict = {
            'data': 'Balance was replenished successfully.'
        }
        return Response(data=response, status=200)

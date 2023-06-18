# Django
from django.urls import path

# Local
from .views import (
    ShowCardsView,
    CreateCardView,
    DoTransactionView,
    ShowTransactionsView,
    ConvertCurrencyView,
    BalanceReplenishmentView,
)


urlpatterns = [
    # Show all cards of user
    path('cards/', ShowCardsView.as_view()),

    # Create new card
    path('new-card/', CreateCardView.as_view()),

    # Do transaction
    path('do-transaction/', DoTransactionView.as_view()),

    # Show all transactions
    path('transactions/', ShowTransactionsView.as_view()),

    # Convert balance from one currency to another
    path('convert-currency/', ConvertCurrencyView.as_view()),

    # Convert balance from one currency to another
    path('balance-replenishment/', BalanceReplenishmentView.as_view()),
]

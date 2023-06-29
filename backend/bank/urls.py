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
    BalanceWithdrawView,
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

    # Replenish balance on user virtual card
    path('balance-replenishment/', BalanceReplenishmentView.as_view()),

    # Withdraw balance on user real card
    path('balance-withdraw/', BalanceWithdrawView.as_view()),
]

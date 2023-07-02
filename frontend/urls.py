# Django
from django.urls import path

# Local
from .views import (
    HomePageView,
    RegistrationView,
    AccountActivationView,
    AccountActivationBaseView,
    LoginView,
    InformationView,
    ForgotPasswordView,
    ProfileView,
    ReplenishBalanceView,
    NewPasswordView,
    TransactionView,
    TransactionAllView,
    WithdrawMoneyView,
    CurrencyConvertationView,
)


urlpatterns = [
    # Homepage
    path('', HomePageView.as_view()),

    # Registration
    path('reg/', RegistrationView.as_view()),

    # Account activation base
    path('account/activation/', AccountActivationBaseView.as_view()),

    # Account activation
    path('account/activation/<str:email>/', AccountActivationView.as_view()),

    # Login user
    path('login/', LoginView.as_view()),

    # Privacy policy
    path('information/', InformationView.as_view()),

    # Forgot password
    path('forgot-password/', ForgotPasswordView.as_view()),

    # Forgot password
    path('account/', ProfileView.as_view()),

    # Replenish balance
    path('balance-replenishment/', ReplenishBalanceView.as_view()),

    # Replenish balance
    path('new-password/', NewPasswordView.as_view()),

    # Do transaction.
    path('transaction/', TransactionView.as_view()),

    # Check all transactions.
    path('transaction/all/', TransactionAllView.as_view()),

    # Withdraw money
    path('withdraw/', WithdrawMoneyView.as_view()),

    # Convert currency
    path('currency-convertation/', CurrencyConvertationView.as_view())
]

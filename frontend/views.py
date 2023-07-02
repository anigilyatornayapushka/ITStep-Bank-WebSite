# Django
from django import views
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render

# Python
import typing as t


class DefaultFrontendView(views.View):
    """
    Default view that implements base logic of views.
    """

    template: str = 'base.html'

    def get(self, request: HttpRequest, *args: t.Any, **kwargs: t.Any
            ) -> HttpResponse:
        """
        GET method.
        """
        return render(request=request, template_name=self.template)


class HomePageView(DefaultFrontendView):
    """
    Home page.
    """

    template: str = 'homepage.html'


class RegistrationView(DefaultFrontendView):
    """
    Registration.
    """

    template: str = 'reg.html'


class AccountActivationBaseView(DefaultFrontendView):
    """
    Activate user account.
    """

    template: str = 'base-account-activation.html'


class AccountActivationView(DefaultFrontendView):
    """
    Activate user account.
    """

    template: str = 'account-activation.html'


class LoginView(DefaultFrontendView):
    """
    Login user in system.
    """

    template: str = 'login.html'


class InformationView(DefaultFrontendView):
    """
    Privacy policy and Terms of use.
    """

    template: str = 'information.html'


class ForgotPasswordView(DefaultFrontendView):
    """
    Password recovery.
    """

    template: str = 'forgot-password.html'


class ProfileView(DefaultFrontendView):
    """
    Profile of user.
    """

    template: str = 'profile.html'


class ReplenishBalanceView(DefaultFrontendView):
    """
    Replenish virtual card balance.
    """

    template: str = 'balance-replenishment.html'


class NewPasswordView(DefaultFrontendView):
    """
    Change user password.
    """

    template: str = 'new-password.html'


class TransactionView(DefaultFrontendView):
    """
    Do transaction.
    """

    template: str = 'transaction.html'



class TransactionAllView(DefaultFrontendView):
    """
    Check all transactions done.
    """

    template: str = 'transaction-all.html'


class WithdrawMoneyView(DefaultFrontendView):
    """
    Withdraw money.
    """

    template: str = 'withdraw.html'


class CurrencyConvertationView(DefaultFrontendView):
    """
    Convert currency.
    """

    template: str = 'currency-convertation.html'

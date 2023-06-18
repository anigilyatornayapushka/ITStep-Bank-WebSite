# Django
from django import views
from django.shortcuts import render
from django.http.request import HttpRequest
from django.http.response import HttpResponse

# Local
from .forms import (
    RegistrationForm,
    LoginForm,
    ActivateAccountForm,
    SendPasswordCodeForm,
    ChangePasswordForm,
    ForgetPasswordForm,
)

# Python
import typing as t


class DefaultFrontendView(views.View):
    """
    Default view that implements base logic of views.
    """

    _form: t.Any = ''
    _context: dict = {}

    def get(self, request: HttpRequest, *args: t.Any, **kwargs: t.Any
            ) -> HttpResponse:
        """
        GET method.
        """
        if self._form:
            context: dict = {
                'ctx_form': self._form
            }
        else:
            context: dict = self._context

        return render(request=request, template_name=self._template,
                      context=context)


class BaseView(DefaultFrontendView):
    """
    Empty page with navigation bar.
    """

    _template: str = 'base.html'


class RegistrationView(DefaultFrontendView):
    """
    View for user to registrate.
    """

    _form: RegistrationForm = RegistrationForm
    _template: str = 'reg.html'


class LoginView(DefaultFrontendView):
    """
    View for user to log in.
    """

    _form: LoginForm = LoginForm
    _template: str = 'login.html'


class AccountActivationView(DefaultFrontendView):
    """
    View for user to activate account.
    """

    _form: ActivateAccountForm = ActivateAccountForm
    _template: str = 'account-activate.html'


class ForgetPasswordView(DefaultFrontendView):
    """
    View for user to restore password.
    """

    _context: dict = {
        'ctx_form1': SendPasswordCodeForm,
        'ctx_form2': ForgetPasswordForm
    }
    _template: str = 'restore-password.html'


class LogoutView(DefaultFrontendView):
    """
    View for user to log out.
    """

    _template: str = 'logout.html'


class ChangePasswordView(DefaultFrontendView):
    """
    View for user to change password.
    """

    _form: ChangePasswordForm = ChangePasswordForm
    _template: str = 'changepassword/change-password.html'


class BankView(DefaultFrontendView):
    """
    View for user to use bank application.
    """

    _template: str = 'bank/bank.html'

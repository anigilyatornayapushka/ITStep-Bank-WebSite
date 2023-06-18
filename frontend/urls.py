# Django
from django.urls import path

# Local
from .views import (
    BaseView,
    RegistrationView,
    LoginView,
    AccountActivationView,
    ForgetPasswordView,
    LogoutView,
    ChangePasswordView,
    BankView,
)


urlpatterns = [
    # Homepage
    path('', BaseView.as_view()),

    # Registration
    path('reg/', RegistrationView.as_view()),

    # Logging in
    path('login/', LoginView.as_view()),

    # Activate account
    path('account-activate/', AccountActivationView.as_view()),

    # Restore password
    path('restore-password/', ForgetPasswordView.as_view()),

    # Logging out
    path('logout/', LogoutView.as_view()),

    # Change password
    path('password-change/', ChangePasswordView.as_view()),

    # Main application
    path('bank/', BankView.as_view()),
]

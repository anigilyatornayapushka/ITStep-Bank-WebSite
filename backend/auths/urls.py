# Django
from django.urls import path

# Local
from .views import (
    RefreshTokenView,
    RegistrationView,
    GetTokenView,
    ActivateAccountView,
    ChangePasswordView,
    ForgotPasswordView,
    NewPasswordConfirmView,
    LogoutView,
    UserView,
    IsAuthView,
)


urlpatterns = [
    # Registration of account
    path('registration/', RegistrationView.as_view()),

    # Get token pair access-refresh
    path('token/', GetTokenView.as_view()),

    # Refresh access token
    path('token/refresh/', RefreshTokenView.as_view()),

    # Activate account after registration
    path('account/activation/', ActivateAccountView.as_view()),

    # Reset password of user
    path('new-password/', ChangePasswordView.as_view()),

    # Reset password of user
    path('password-recovery/', ForgotPasswordView.as_view()),

    # Reset password of user
    path('password-recovery/confirmation/', NewPasswordConfirmView.as_view()),

    # Delete refresh token
    path('logout/', LogoutView.as_view()),

    # User info
    path('user/', UserView.as_view()),

    # If user was authenticated
    path('authentication-check/', IsAuthView.as_view()),
]

# Django
from django.urls import path

# Local
from .views import (
    RefreshTokenView,
    RegistrationView,
    GetTokenView,
    ActivateAccountView,
    ChangePasswordView,
    ForgetPasswordView,
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

    # Confirm account after registration
    path('account/confirm/', ActivateAccountView.as_view()),

    # Reset password of user
    path('password/change/', ChangePasswordView.as_view()),

    # Reset password of user
    path('password/forget/', ForgetPasswordView.as_view()),

    # Reset password of user
    path('password/reset/', NewPasswordConfirmView.as_view()),

    # Delete all refresh tokens
    path('logout/', LogoutView.as_view()),

    # User info
    path('user/', UserView.as_view()),

    # If user was authenticated
    path('is-auth/', IsAuthView.as_view()),
]

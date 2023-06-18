# DRF
from rest_framework.request import Request

# Django
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth import get_user_model

# Simple JWT
from rest_framework_simplejwt.authentication import JWTAuthentication


User: AbstractBaseUser = get_user_model()


class AccessTokenMixin:
    """
    Mixin, that helps to work with access token.
    """

    def get_user(self, request: Request) -> tuple[User, dict | None]:
        """
        Use only with IsAuthenticated in permissions_classes.
        """
        # Define error to return then
        error: None = None

        # If token wasn't given, return error
        if not request.auth:
            error: dict = {
                'token': ['token is not valid.']
            }

        # Authenticate token
        authenticator: JWTAuthentication = JWTAuthentication()
        user: User = authenticator.get_user(request.auth)

        return user, error

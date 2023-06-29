# Django
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth import get_user_model

# DRF
from rest_framework.request import Request

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
        # Authenticate token
        authenticator: JWTAuthentication = JWTAuthentication()
        user: User = authenticator.get_user(request.auth)

        return user

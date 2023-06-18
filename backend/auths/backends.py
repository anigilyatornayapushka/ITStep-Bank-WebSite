# Django
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth import get_user_model

# DRF
from rest_framework.request import Request


User: AbstractBaseUser = get_user_model()


class UserBackend(ModelBackend):
    """
    Backend for user to authenticate.
    """

    def authenticate(self, request: Request, email: str = '',
                     password: str = '', **kwargs: dict
                     ) -> User | None:
        """
        Custom user authenticate method.
        """
        user: User

        # Find user with email=email and check if password is correct
        if user := User.objects.get_object_or_none(email=email):

            # Check if user password is valid
            if user.check_password(password):
                return user

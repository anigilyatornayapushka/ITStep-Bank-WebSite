# Django
from django.utils import timezone

# JWT
from rest_framework_simplejwt.settings import USER_SETTINGS

# Python
import typing as t
import datetime

# Local
from ..models import TokenWhiteList
from ..utils import Sha256Hasher


def check_refresh_token_validity(refresh_token: str) -> bool:
    """
    Check if refresh token is registered in database.
    """
    # Define hasher
    hasher: Sha256Hasher = Sha256Hasher()

    # Hash token to check it is in database
    hashed_refresh_token: str = hasher.hash(refresh_token)

    exists: bool = TokenWhiteList.objects.filter(
        refresh_token=hashed_refresh_token).exists()

    return exists


def add_token_to_db(**kwargs: t.Any) -> None:
    """
    Create refresh token function. Kwargs must contain

    user, token, ip, fingerprint.
    """
    # Get all user tokens
    tokens = TokenWhiteList.objects.filter(user=kwargs.get('user')).only('id')

    # If user has more than 4 tokens, delete them
    if tokens.count() >= 5:
        tokens.delete()

    # Generate expiration datetime
    datetime_expire: datetime.datetime =\
        timezone.now() + USER_SETTINGS.get('REFRESH_TOKEN_LIFETIME')

    # Define hasher
    hasher: Sha256Hasher = Sha256Hasher()
    token: str = kwargs.get('token')

    # Add new token in database
    TokenWhiteList.objects.create(
        user=kwargs.get('user'),
        refresh_token=hasher.hash(token),
        expire_datetime=datetime_expire,
        fingerprint=kwargs.get('fingerprint'),
        ip=kwargs.get('ip')
    )

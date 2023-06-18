# Python
import typing as t
import datetime

# Local
from ..models import TokenWhiteList

# JWT
from rest_framework_simplejwt.settings import USER_SETTINGS

# Django
from django.utils import timezone


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

    # Add new token in database
    TokenWhiteList.objects.create(
        user=kwargs.get('user'),
        refresh_token=kwargs.get('token'),
        expire_datetime=datetime_expire,
        fingerprint=kwargs.get('fingerprint'),
        ip=kwargs.get('ip')
    )

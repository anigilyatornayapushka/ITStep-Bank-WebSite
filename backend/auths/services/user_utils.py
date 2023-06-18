# DRF
from rest_framework.request import Request


def get_user_ip(request: Request) -> str:
    """
    Get user ip.
    """
    # Get ip from request META
    ip: str = request.META.get('HTTP_X_FORWARDED_FOR') or\
        request.META.get('REMOTE_ADDR', '')

    return ip

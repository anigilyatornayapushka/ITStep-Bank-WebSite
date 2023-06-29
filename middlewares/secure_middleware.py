# Django
from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponse

# Python
import typing as t


class SecureMiddleware:

    def __init__(self, get_response: t.Callable) -> None:
        self.get_response = get_response

    def __call__(self, request: WSGIRequest) -> HttpResponse:

        # Create response
        response: HttpResponse = self.get_response(request)

        # Set headers anti XSS
        response['X-Frame-Options'] = 'SAMEORIGIN'
        response['X-Content-Type-Options'] = 'nosniff'

        # Set httpOnly cookie refresh_token
        if request.META.get('HTTP_REFERER') == 'http://127.0.0.1:8000/login/':

            # If data
            if 'data' in dir(response):

                # If success response
                if response.status_code < 300 and response.status_code >= 200:

                    # Define token lifetime
                    long_lifetime: bool = request.POST.get('remember_me')

                    # Params for cookie
                    params: dict = {
                        'httponly': True,
                        'samesite': 'Strict',
                        'path': '/'
                    }

                    # If long time is True
                    if long_lifetime == 'true':

                        # Define token expiration
                        expiration: int = 60 * 60 * 24 * 7 # 1 week
                        expiration -= 60 # Take away one minute just in case

                        params['max_age'] = expiration

                    else:

                        # Add expire=Session into cookie
                        params['max_age'] = None
                        params['expires'] = None

                    # Define token
                    refresh_token: str = response.data.get('refresh')

                    # If logging in was successfull
                    if refresh_token:

                        # Set cookie
                        response.set_cookie('refresh_token', refresh_token,
                                            **params)

        # Delete resfresh_token from cookie
        elif request.META.get('HTTP_REFERER') == 'http://127.0.0.1:8000/logout/':

            # If data
            if 'data' in dir(response):

                # If success response
                if response.status_code == 200:

                    response.delete_cookie('refresh_token')

        return response

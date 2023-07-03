# DRF
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import generics

# Python
import typing as t

# Third-party
from abstracts.mixins import AccessTokenMixin

# Local
from .serializers import (
    RegistrateUserSerializer,
    LoginUserSerializer,
    ActivateAccountSerializer,
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    ConfirmPasswordSerializer,
    RefreshTokenSerializer,
    LogoutSerializer,
    UserSerializer,
)
from .services.token_utils import check_refresh_token_validity


class CommonPostView(generics.GenericAPIView):
    """
    View for processing post method with common logic.

    Serializer_class must match next pattern:

>>> class Serializer(serializer.Serializer):
>>>     \"\"\"Docstring.\"\"\"
>>>
>>>    def is_valid(self, attrs: dict) -> dict:
>>>         # Validation with exception raising
>>>         return attrs
>>>
>>>     def save(self) -> None:
>>>         # Save data
>>>
>>>     def get_response(self) -> dict:
>>>         # Return response to the view
    """

    permission_classes: tuple = (AllowAny,)
    serializer_class: t.Any = ...
    success_status: int = 200

    def post(self, request: Request) -> Response:
        """
        POST request.
        """
        # Data deserialization
        serializer = self.serializer_class(data=request.data)

        # Set attribute .request in serializer. We need it then
        serializer.request = request

        # Do validation of data. Raise exceptions
        serializer.is_valid(raise_exception=True)

        # Save data
        serializer.save()

        # Get response from serializer (Custom method)
        response = serializer.get_response()

        # Return message
        return Response(data=response, status=self.success_status)


class RegistrationView(CommonPostView):
    """
    User registration view.
    """

    permission_classes: tuple = (AllowAny,)
    serializer_class: RegistrateUserSerializer = RegistrateUserSerializer
    success_status: int = 202


class GetTokenView(CommonPostView):
    """
    User login and get tokens view.
    """

    permission_classes: tuple = (AllowAny,)
    serializer_class: LoginUserSerializer = LoginUserSerializer
    success_status: int = 200


class RefreshTokenView(CommonPostView):
    """
    Refresh access token using refresh token.
    """

    permission_classes: tuple = (AllowAny,)
    serializer_class: RefreshTokenSerializer = RefreshTokenSerializer
    success_status: int = 200


class ActivateAccountView(CommonPostView):
    """
    Refresh access token using refresh token.
    """

    permission_classes: tuple = (AllowAny,)
    serializer_class: ActivateAccountSerializer = ActivateAccountSerializer
    success_status: int = 200


class ChangePasswordView(CommonPostView):
    """
    Change user password view.
    """

    permission_classes: tuple = (IsAuthenticated,)
    serializer_class: ChangePasswordSerializer = ChangePasswordSerializer
    success_status: int = 200


class ForgotPasswordView(CommonPostView):
    """
    Get reset password code for user.
    """

    permission_classes: tuple = (AllowAny,)
    serializer_class: ForgotPasswordSerializer = ForgotPasswordSerializer
    success_status: int = 200


class NewPasswordConfirmView(CommonPostView):
    """
    Confirm new password code for user.
    """

    permission_classes: tuple = (AllowAny,)
    serializer_class: ConfirmPasswordSerializer = ConfirmPasswordSerializer
    success_status: int = 200


class LogoutView(CommonPostView):
    """
    Logout view.
    """

    permission_classes: tuple = (IsAuthenticated,)
    serializer_class: LogoutSerializer = LogoutSerializer
    success_status: int = 200


class UserView(generics.GenericAPIView, AccessTokenMixin):
    """
    User information view.
    """

    permission_classes: tuple = (IsAuthenticated,)
    serializer_class: UserSerializer = UserSerializer
    success_status: int = 200

    def get(self, request: Request) -> Response:
        """
        GET request.
        """
        user = self.get_user(request=request)
        serializer = self.serializer_class(instance=user)
        return Response(data=serializer.data, status=self.success_status)


class IsAuthView(generics.GenericAPIView, AccessTokenMixin):
    """
    View to check if user authenticated.
    """

    permission_classes: tuple = (AllowAny,)
    success_status: int = 200

    def get(self, request: Request) -> Response:
        """
        GET request.
        """
        # Get refresh_token from cookies
        refresh_token: str = request.COOKIES.get('refresh_token')

        # Check if refresh token is not valid
        if check_refresh_token_validity(refresh_token=refresh_token) is False:
            return Response(status=400)

        return Response(status=self.success_status)

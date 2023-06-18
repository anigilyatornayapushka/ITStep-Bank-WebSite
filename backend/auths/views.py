# DRF
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import generics

# Local
from .serializers import (
    RegistrateUserSerializer,
    LoginUserSerializer,
    ActivateAccountSerializer,
    ChangePasswordSerializer,
    ForgetPasswordSerializer,
    ConfirmPasswordSerializer,
    RefreshTokenSerializer,
    LogoutSerializer,
    UserSerializer,
)

# Python
import typing as t

# Third-party
from abstracts.mixins import AccessTokenMixin


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
        POST method.
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


class ForgetPasswordView(CommonPostView):
    """
    Get reset password code for user.
    """

    permission_classes: tuple = (AllowAny,)
    serializer_class: ForgetPasswordSerializer = ForgetPasswordSerializer
    success_status: int = 200


class NewPasswordConfirmView(CommonPostView):
    """
    Confirm new password code for user.
    """

    permission_classes: tuple = (AllowAny,)
    serializer_class: ConfirmPasswordSerializer = ConfirmPasswordSerializer
    success_status: int = 200


class LogoutView(CommonPostView):
    """"
    Logout view.
    """

    permission_classes: tuple = (IsAuthenticated,)
    serializer_class: LogoutSerializer = LogoutSerializer
    success_status: int = 200


class UserView(CommonPostView, AccessTokenMixin):
    """"
    User information view.
    """

    permission_classes: tuple = (IsAuthenticated,)
    serializer_class: UserSerializer = UserSerializer
    success_status: int = 200

    def post(self, request: Request) -> Response:
        user, _ = self.get_user(request=request)
        serializer = self.serializer_class(instance=user)
        return Response(data=serializer.data, status=self.success_status)


class IsAuthView(CommonPostView, AccessTokenMixin):
    """"
    View to check if user authenticated.
    """

    permission_classes: tuple = (IsAuthenticated,)
    success_status: int = 200

    def post(self, request: Request) -> Response:
        data: dict = {
            'data': 'ok'
        }
        return Response(data=data, status=self.success_status)

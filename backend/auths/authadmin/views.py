# DRF
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny

# Third-party
from ..views import CommonPostView

# Local
from ..serializers import LoginUserSerializer


class AdminUserLogin(CommonPostView, GenericAPIView):
    """
    View to authenticate and login admin user.
    """

    permission_classes: tuple = (AllowAny,)
    serializer_class: LoginUserSerializer = LoginUserSerializer
    success_status: int = 200

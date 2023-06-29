# Django
from django.urls import path

# Local
from .views import AdminUserLogin


urlpatterns = [
    # Custom log in view, because default view
    # doesn't work for some reason.
    path('login/', AdminUserLogin.as_view()),
]

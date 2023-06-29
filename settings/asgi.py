# Django
from django.core.handlers.asgi import ASGIHandler
from django.core.asgi import get_asgi_application

# Python
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.base')

application: ASGIHandler = get_asgi_application()

# Python
import os

# Django
from django.core.wsgi import get_wsgi_application
from django.core.handlers.wsgi import WSGIHandler


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.base')

application: WSGIHandler = get_wsgi_application()

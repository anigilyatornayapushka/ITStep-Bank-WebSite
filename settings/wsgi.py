# Django
from django.core.handlers.wsgi import WSGIHandler
from django.core.wsgi import get_wsgi_application

# Python
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.base')

application: WSGIHandler = get_wsgi_application()

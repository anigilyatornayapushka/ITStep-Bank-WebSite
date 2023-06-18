# Python
import os

# Celery
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.base')

app = Celery('settings')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

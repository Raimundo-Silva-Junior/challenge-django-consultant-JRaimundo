import os
from celery import Celery
from django.apps import apps


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_backend.settings')

app = Celery('django_backend')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

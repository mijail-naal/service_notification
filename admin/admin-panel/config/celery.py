import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# broker='amqp://guest:guest@rabbitmq:5672'
app = Celery('config')  # broker=broker
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

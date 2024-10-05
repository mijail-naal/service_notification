from celery import Celery
from core.config import rabbit_settings as rs


broker = f'amqp://{rs.user}:{rs.password}@{rs.host}'

app = Celery('deliver', broker=broker, include=['deliver.tasks'])
app.autodiscover_tasks()

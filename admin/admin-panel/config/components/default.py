# import os


# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS').split(',')


EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = os.environ.get('EMAIL_PORT')


CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')

# DJANGO_SUPERUSER_USERNAME=os.environ.get('DJANGO_SUPERUSER_USERNAME')
# DJANGO_SUPERUSER_EMAIL=os.environ.get('DJANGO_SUPERUSER_EMAIL')
# DJANGO_SUPERUSER_PASSWORD=os.environ.get('DJANGO_SUPERUSER_PASSWORD')

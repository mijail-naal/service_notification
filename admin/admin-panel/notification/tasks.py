from celery import shared_task
from django.core.mail import send_mail
from .models import Notification


@shared_task
def notification_created(notification_id):
    """Task to send an e-mail notification.

    The notification is sent when an order is
    successfully created.
    """
    notification = Notification.objects.get(id=notification_id)
    subject = f'Notification nr. {notification.id}'
    message = (
        f'Dear {notification.first_name},\n\n'
        f'You have successfully paid for your plan. '
        f'Your order ID is {notification.pk}.'
    )
    mail_sent = send_mail(
        subject, message, 'admin@mail.com', [notification.email]
    )
    return mail_sent

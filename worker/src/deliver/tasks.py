import json

from pydantic import BaseModel

from celery import shared_task
from .noti_email import Notification


class TestNotification(BaseModel):
    """This class emulates the data we receive
    from the Auth-service.

    With the user ID we can make a requests to
    the database and receive the username and email 
    to send a notification.

    The recipient, template name, event type, and
    content, we receive from Rabbit and prepare all
    the data to send a notification by email with
    the task 'send_notification'.
    """

    id: int = '12345'
    username: str = 'John'
    email: str = 'test@mail.com'
    users: list = ['John']
    template: str = 'new_registration'
    event: str = 'new_registration'
    content: dict = {}


cn = TestNotification()


@shared_task
def send_notification(body):
    decoded = body.decode('utf-8')
    data = json.loads(decoded)
    notification = Notification()
    notification.send_email(cn)

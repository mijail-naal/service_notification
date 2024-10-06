import json
import requests

from uuid import UUID

from pydantic import BaseModel

from celery import shared_task
from .noti_email import Notification
from core.config import settings


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

    id: UUID = 'c3242d9b-4ff7-494e-9cc4-4fc9842c0ba1'
    username: str = 'John'
    email: str = 'test@mail.com'
    users: list = ['John']
    template: str = 'new_registration'
    event: str = 'new_registration'
    content: dict = {}


cn = TestNotification()


def get_user_from_auth(user_id):
    auth = requests.post(
        settings.auth_signin_url,
        json={'username': settings.auth_admin_name, 'password': settings.auth_password}
    )
    tokens = json.loads(auth.content)
    res = requests.post(
        settings.auth_get_user_url,
        headers={
            'Authorization': 'Bearer {access_token}'.format(
                access_token=tokens['access_token']
            )
        },
        json={'id': user_id}
    )
    return res.content.decode('utf-8')


@shared_task
def send_notification(body):
    decoded = body.decode('utf-8')
    data = json.loads(decoded)
    user = get_user_from_auth(data['id'])
    cn.id = user['id']
    cn.username = user['first_name']
    cn.email = user['email']
    notification = Notification()
    notification.send_email(cn)

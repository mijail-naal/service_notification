import os
# import sys
import logging
import smtplib

from email.message import EmailMessage

from jinja2 import FileSystemLoader, Environment
from pydantic import BaseModel, EmailStr

# sys.path.append('..')
from core.config import settings


logger = logging.getLogger('__name__')


class EmailNotification(BaseModel):
    users: list
    template: str
    event: str
    content: dict


class UserModel(BaseModel):
    id: int
    username: str
    email: EmailStr


class UserNotification(UserModel, EmailNotification):
    pass


class Notification:
    """Class to make and send a notification."""

    def __init__(self):
        self.loader = FileSystemLoader(os.path.dirname(__file__))
        self.environment = Environment(loader=self.loader)

    def create_notification(self, notification: UserNotification) -> EmailMessage:
        data = {
            'title': f'Wellcome {notification.username}!\n\n',
            'message': 'Thanks to join us.',
        }

        message = EmailMessage()
        message['From'] = settings.email_sender
        message['To'] = ','.join([notification.email])
        message['Subject'] = 'Wellcome'

        template = self.environment.get_template(f'templates/{notification.template}.html')
        output = template.render(**data)
        message.add_alternative(output, subtype='html')
        return message

    def send_email(self, notification: UserNotification):
        notification = self.create_notification(notification)
        if not notification:
            return

        # server = smtplib.SMTP_SSL(settings.smtp_host, settings.smtp_port)
        server = smtplib.SMTP(settings.smtp_host, settings.smtp_port)

        try:
            server.sendmail(notification['from'], notification['To'], notification.as_string())
        except smtplib.SMTPException as exc:
            reason = f'{type(exc).__name__}: {exc}'
            logger.error(f'Can not send the email. {reason}')
        else:
            logger.info('Email sent!')
        finally:
            server.close()


if __name__ == '__main__':

    class TestNotification(BaseModel):
        id: int = '12345'
        username: str = 'AN'
        email: str = 'test@test.test'
        users: list = ['AN']
        template: str = 'string'
        event: str = 'new_registration'
        content: dict = {}

    cn = TestNotification()

    n = Notification()
    n.send_email(cn)

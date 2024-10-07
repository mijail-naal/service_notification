from http import HTTPStatus

from fastapi import APIRouter, Depends
from pymongo import MongoClient

from services.broker import BrokerService, get_broker_service
from schemas.email import EmailNotification
from services.storage import MongoStorage
from core.config import settings


router = APIRouter()
client = MongoClient(settings.mongo_host, settings.mongo_port)
mongo_storage = MongoStorage(client)


@router.post('/email-notification', response_model=dict, status_code=HTTPStatus.OK)
async def send_email_notification(
    notification: EmailNotification,
    broker_service: BrokerService = Depends(get_broker_service),
) -> dict[str, str]:
    """Endpoint to receive information about the email notification."""
    
    await broker_service.send_to_broker(notification)
    collection = mongo_storage.connect('UsersDB', 'Notification')
    mongo_storage.insert(collection, notification.model_dump())
    return {'msg': 'notification sent to broker'}

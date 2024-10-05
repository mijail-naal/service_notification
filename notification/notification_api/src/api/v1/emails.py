from http import HTTPStatus

from fastapi import APIRouter, Depends
# from sqlalchemy.ext.asyncio import AsyncSession

# from db.postgres import get_session
from services.broker import BrokerService, get_broker_service
from schemas.email import EmailNotification


router = APIRouter()


@router.post('/email-notification', response_model=dict, status_code=HTTPStatus.OK)
async def send_email_notification(
    notification: EmailNotification,
    broker_service: BrokerService = Depends(get_broker_service),
    # db: AsyncSession = Depends(get_session),
) -> dict[str, str]:
    """Endpoint to receive information about the email notification."""
    # print(notification)
    # print(type(notification))
    await broker_service.send_to_broker(notification)
    return {'msg': 'notification sent to broker'}

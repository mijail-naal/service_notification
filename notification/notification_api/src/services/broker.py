from functools import lru_cache

from fastapi import Depends
from aio_pika import Message, Connection

from schemas.email import EmailNotification
from core.config import rabbit_settings as rs
from db.rabbit import get_conection, get_channel, get_exchange


class BrokerService:
    def __init__(self, connection, channel, exchange) -> None:
        self.connection = connection
        self.channel = channel
        self.exchange = exchange

    async def send_message(self, queue_name: str, data: EmailNotification):
        message = Message(
            body=data.model_dump_json().encode('utf-8'),
            delivery_mode=rs.delivery_mode,
        )
        queue = await self.channel.declare_queue(name=queue_name, durable=True)
        await queue.bind(self.exchange)
        await self.exchange.publish(routing_key=queue_name, message=message)

    async def send_to_broker(self, event: EmailNotification):
        print(event)
        print(type(event))
        await self.send_message(queue_name=f'email.{event.event}', data=event)


@lru_cache()
def get_broker_service(
    connection: Connection = Depends(get_conection),
    channel: Connection = Depends(get_channel),
    exchange: Connection = Depends(get_exchange)
) -> BrokerService:
    return BrokerService(connection, channel, exchange)

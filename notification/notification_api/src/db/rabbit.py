from aio_pika import Connection, Channel, Exchange


connection: Connection | None = None
channel: Channel | None = None
exchange: Exchange | None = None


async def get_conection():
    return connection


async def get_channel():
    return channel


async def get_exchange():
    return exchange

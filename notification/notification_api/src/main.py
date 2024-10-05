import logging
import uvicorn

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from aio_pika import connect_robust

from api.v1 import emails
from core.config import settings, rabbit_settings as rs
from core.logger import LOGGING
from db import rabbit


@asynccontextmanager
async def lifespan(app: FastAPI):
    rabbit.connection = await connect_robust(f'amqp://{rs.user}:{rs.password}@{rs.host}/')
    rabbit.channel = await rabbit.connection.channel()
    rabbit.exchange = await rabbit.channel.declare_exchange(rs.exchange)
    yield
    await rabbit.channel.close()
    await rabbit.connection.close()


app = FastAPI(
    title=settings.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
    debug=True
)


app.include_router(emails.router, prefix='/api/v1/users', tags=['users'])


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8001,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=True
    )

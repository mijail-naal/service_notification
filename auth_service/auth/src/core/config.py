import os
from logging import config as logging_config

from core.logger import LOGGING

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='../env/prod/.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )
    project_name: str = ...
    redis_host: str = Field(9200, alias='REDIS_HOST')
    redis_port: int = Field(6379, alias='REDIS_PORT')
    authjwt_key: str = ...
    echo_var: bool = ...
    debug: bool = ...
    service_name: str = ...
    secret_key: str = ...


settings = Settings()


class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix='postgres_',
        env_file='../env/prod/.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )
    db: str = ...
    user: str = ...
    password: str = ...
    host: str = ...
    port: int = ...


pg = PostgresSettings()

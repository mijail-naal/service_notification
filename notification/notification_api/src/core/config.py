from logging import config as logging_config

from pydantic_settings import BaseSettings, SettingsConfigDict

from core.logger import LOGGING


logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='../env/prod/.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )
    project_name: str = ...
    authjwt_key: str = ...
    echo_var: bool = ...
    debug: bool = ...
    secret_key: str = ...


settings = Settings()


class RabbitSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix='rabbit_',
        env_file='../env/prod/.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )
    host: str = ...
    port: int = ...
    user: str = ...
    password: str = ...
    delivery_mode: str = ...
    exchange: str = ...


rabbit_settings = RabbitSettings()

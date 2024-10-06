from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / '.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )
    project_name: str = ...
    authjwt_key: str = ...
    echo_var: bool = ...
    debug: bool = ...
    secret_key: str = ...
    email_sender: str = Field('test@mail.com', alias='EMAIL_SENDER')
    smtp_host: str = Field('mailhog', alias='SMTP_HOST')
    smtp_port: int = Field(1025, alias='SMTP_PORT')
    auth_signin_url: str = ...
    auth_get_user_url: str = ...
    auth_admin_name: str = ...
    auth_password: str = ...


settings = Settings()


class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix='postgres_',
        env_file=BASE_DIR / '.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )
    db: str = ...
    user: str = ...
    password: str = ...
    host: str = ...
    port: int = ...


pg = PostgresSettings()


class RabbitSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix='rabbit_',
        env_file=BASE_DIR / '.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )
    host: str = Field('rabbitmq', alias='RABBIT_HOST')
    port: int = Field(5672, alias='RABBIT_PORT')
    user: str = Field('guest', alias='RABBIT_USER')
    password: str = Field('guest', alias='RABBIT_PASSWORD')
    delivery_mode: str = Field(2, alias='RABBIT_DELIVERY_MODE')
    exchange: str = Field('emails', alias='RABBIT_EXCHANGE')
    queue: str = Field('email.new_registration', alias='RABBIT_QUEUE')


rabbit_settings = RabbitSettings()

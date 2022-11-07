import os
from typing import Optional, Union

from dotenv import load_dotenv
from pydantic import BaseSettings, BaseModel

IS_DOCKER = os.environ.get('AM_I_IN_A_DOCKER_CONTAINER', False)

if not IS_DOCKER:
    load_dotenv()   # take environment variables from .env.


class KafkaPromSettings(BaseModel):
    KAFKA_HOST: Optional[str] = os.getenv('KAFKA_HOST')
    KAFKA_PORT: Optional[str]  = os.getenv('KAFKA_PORT')


class KafkaDevSettings(BaseModel):
    KAFKA_HOST: Optional[str] = os.getenv('KAFKA_HOST_DEBUG')
    KAFKA_PORT: Optional[str] = os.getenv('KAFKA_PORT_DEBUG')


class PostgresqlUser(BaseModel):
    POSTGRES_USER: Optional[str] = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD: Optional[str] = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_DB: Optional[str] = os.getenv('POSTGRES_DB')
    POSTGRES_PORT: Optional[str] = os.getenv('POSTGRES_PORT')


class PostgresqlPromSettings(PostgresqlUser):
    POSTGRES_HOST: Optional[str] = os.getenv('POSTGRES_HOST')


class PostgresqlDevSettings(PostgresqlUser):
    POSTGRES_HOST: Optional[str] = os.getenv('POSTGRES_HOST_DEBUG')


class Settings(BaseSettings):

    TOPIC: Optional[str] = os.getenv('TOPIC')
    BATCH_SIZE: int

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


class PromSettings(Settings):
    kafka_settings: KafkaPromSettings = KafkaPromSettings()
    postgres_settings: PostgresqlPromSettings = PostgresqlPromSettings()


class DevSettings(Settings):
    kafka_settings: KafkaDevSettings = KafkaDevSettings()
    postgres_settings: PostgresqlDevSettings = PostgresqlDevSettings()


def get_settings() -> Union[PromSettings, DevSettings]:
    environment = os.getenv('ENVIRONMENT')
    if environment == 'prom':
        return PromSettings()
    else:
        return DevSettings()


settings = get_settings()

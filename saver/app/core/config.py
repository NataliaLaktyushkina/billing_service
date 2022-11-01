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
    KAFKA_HOST: Optional[str]  = os.getenv('KAFKA_HOST_DEBUG')
    KAFKA_PORT: Optional[str]  = os.getenv('KAFKA_PORT_DEBUG')


class Settings(BaseSettings):

    TOPIC: Optional[str]  = os.getenv('TOPIC')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


class PromSettings(Settings):
    kafka_settings: KafkaPromSettings = KafkaPromSettings()


class DevSettings(Settings):
    kafka_settings: KafkaDevSettings = KafkaDevSettings()


def get_settings() -> Union[PromSettings, DevSettings]:
    environment = os.getenv('ENVIRONMENT')
    if environment == 'prom':
        return PromSettings()
    else:
        return DevSettings()


settings = get_settings()

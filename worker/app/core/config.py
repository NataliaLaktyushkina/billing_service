import os

from dotenv import load_dotenv
from pydantic import BaseSettings

IS_DOCKER = os.environ.get('AM_I_IN_A_DOCKER_CONTAINER', False)

if not IS_DOCKER:
    load_dotenv()   # take environment variables from .env.


class Settings(BaseSettings):

    BATCH_SIZE: int

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


def get_settings() -> Settings:
    return Settings()


settings = get_settings()

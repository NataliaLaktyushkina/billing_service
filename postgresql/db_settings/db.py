"""Модуль содержит вспомогательный функции для работы с базой данных."""
import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from postgresql.db_settings.config_saver import settings


db_settings = settings.postgres_settings

username = db_settings.POSTGRES_USER
password = db_settings.POSTGRES_PASSWORD
host = db_settings.POSTGRES_HOST
port = db_settings.POSTGRES_PORT
host_port = ':'.join((host, port))
database_name = db_settings.POSTGRES_DB

SQLALCHEMY_DATABASE_URI = f'postgresql+asyncpg://{username}:{password}@{host_port}/{database_name}'
ALEMBIC_SQLALCHEMY_DATABASE_URI = f'postgresql://{username}:{password}@{host_port}/{database_name}'


logger = logging.getLogger(__name__)

engine = create_async_engine(SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

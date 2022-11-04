"""Модуль содержит вспомогательный функции для работы с базой данных."""
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from core.config_saver import settings

db_settings = settings.postgres_settings

username = db_settings.POSTGRES_USER
password = db_settings.POSTGRES_PASSWORD
host = db_settings.POSTGRES_HOST
port = db_settings.POSTGRES_PORT
host_port = ':'.join((host, port))
database_name = db_settings.POSTGRES_DB

SQLALCHEMY_DATABASE_URI = f'postgresql://{username}:{password}@{host_port}/{database_name}'


logger = logging.getLogger(__name__)

engine = create_engine(SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

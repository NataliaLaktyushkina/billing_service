from datetime import datetime
import uuid
from typing import Optional

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy import Column, String, Date, DateTime
from sqlalchemy import or_
from sqlalchemy.dialects.postgresql import UUID

from database.db import Base


def create_partition_for_users(target, connection, **kw) -> None:
    """Create users partition by date of birth."""
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS "users_birthdays_1920_to_1979"
        PARTITION OF "users"
        FOR VALUES FROM ('1920-01-01') TO ('1979-12-31');
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS "users_birthdays_1980_to_2003"
        PARTITION OF "users"
        FOR VALUES FROM ('1980-01-01') TO ('2003-12-31');
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS "users_birthdays_2004_to_2022"
        PARTITION OF "users"
        FOR VALUES FROM ('2004-01-01') TO ('2022-12-31');
        """
    )


class User(Base):
    """Model to represent user data """
    __tablename__ = 'users'
    __table_args__ = (
        UniqueConstraint("id", "email", "date_of_birth"),
        {
            "postgresql_partition_by": "RANGE (date_of_birth)",
            "listeners": [("after_create", create_partition_for_users)],
        },
    )

    id = Column(UUID(as_uuid=True), primary_key=True,
                default=uuid.uuid4, unique=True, nullable=False)
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)

    date_of_birth = Column(Date, primary_key=True,
                           default=datetime.today().date())

    def __repr__(self):
        return f'<User {self.login}>'

    @classmethod
    def get_user_by_universal_login(cls, login: Optional[str] = None, email: Optional[str] = None):
        return cls.query.filter(or_(cls.login == login, cls.email == email)).first()


class PaymentsNew(Base):
    """Model to represent history of payments"""
    __tablename__ = 'payments_new'

    id = Column(UUID(as_uuid=True), primary_key=True,
                default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey(User.id))
    payment_id = Column(UUID(as_uuid=True))
    payment_date = Column(DateTime, default=datetime.utcnow(), nullable=False)
    payment_type = Column(String, nullable=False)

    def __repr__(self):
        return f'<Payments {self.user_id}:{self.payment_type}>'

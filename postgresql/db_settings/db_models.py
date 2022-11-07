from datetime import datetime
import uuid
from typing import Optional

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy import Column, String, Date, DateTime, Float
from sqlalchemy import or_
from sqlalchemy.dialects.postgresql import UUID

from postgresql.db_settings.db import Base


class User(Base):
    """Model to represent user data """
    __tablename__ = 'users'
    __table_args__ = (
        UniqueConstraint('id', 'email', 'date_of_birth'),
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


class SubscriptionTypes(Base):
    """Model to represent roles"""
    __tablename__ = 'subscription_types'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String, unique=True, nullable=False)


class SubscriptionCost(Base):
    """Model to represent roles"""
    __tablename__ = 'subscription_cost'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    subscription_type = Column(String, ForeignKey(SubscriptionTypes.name), nullable=False)
    cost = Column(Float(precision=2), nullable=False)
    creation_date = Column(Date, default=datetime.utcnow(), nullable=False)


class PaymentsNew(Base):
    """Model to represent history of payments"""
    __tablename__ = 'payments_new'

    id = Column(UUID(as_uuid=True), primary_key=True,
                default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey(User.id))
    subscription_type = Column(String, ForeignKey(SubscriptionTypes.name), nullable=False)
    payment_date = Column(DateTime, default=datetime.utcnow(), nullable=False)
    payment_type = Column(String, nullable=False)

    def __repr__(self):
        return f'<Payments {self.user_id}:{self.payment_type}>'


class Payments(Base):
    """Model to represent payments to process"""
    __tablename__ = 'payments'

    id = Column(UUID(as_uuid=True), primary_key=True,
                default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey(User.id))
    subscription_type = Column(String, ForeignKey(SubscriptionTypes.name), nullable=False)
    payment_date = Column(DateTime, default=datetime.utcnow(), nullable=False)
    payment_type = Column(String, nullable=False)

    def __repr__(self):
        return f'<Payments {self.user_id}:{self.payment_type}>'

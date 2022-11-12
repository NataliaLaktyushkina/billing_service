import secrets
import string
from typing import List, Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from werkzeug.security import generate_password_hash

from postgresql.db_settings.db import SessionLocal
from postgresql.db_settings.db_models import User, Payments, ProcessingStatus, PaymentStatus
from postgresql.db_settings.logger import logger


def get_user_by_login(login: str) -> User:
    user = User.query.filter_by(login=login).first()
    return user


def generate_password():
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(8))

    return password


def create_user(username, email, password: Optional[str] = None):
    if password is None:
        password = generate_password()
    hashed_password = generate_password_hash(password, method='sha256')
    new_user = User(login=username,
                    password=hashed_password,
                    email=email)
    service = SessionLocal()
    service.add(new_user)
    service.commit()

    return new_user


async def add_payment(payment_data: List[dict]):
    service = SessionLocal()
    for payment in payment_data:
        new_payment = Payments(
            user_id=payment['user_id'],
            subscription_type=payment['subscription_type'],
            processing_status=ProcessingStatus.new,
            payment_date=payment['payment_date'],
            payment_type=payment['payment_type'],
        )
        service.add(new_payment)
    try:
        await service.commit()
    except IntegrityError:
        logger.error(msg='Could not add payment')


async def extract_new_payments() -> List[Payments]:
    async with SessionLocal() as session:
        result = await session.execute(
            select(Payments).filter(
                Payments.processing_status == ProcessingStatus.new,
            ),
        )
        return result.scalars().all()


async def upload_last_payment(processing_status: ProcessingStatus) -> List[Payments]:
    """Choose last request from user in selected processing status"""
    async with SessionLocal() as session:
        result = await session.execute(
            select(Payments).filter(
                Payments.processing_status == processing_status).order_by(Payments.payment_date.desc()),
        )
        return result.scalars().first()


async def update_statuses(
        payment: Payments, processing_status: ProcessingStatus,
        payment_status: PaymentStatus = PaymentStatus.unknown,
) -> None:
    async with SessionLocal() as session:
        result = await session.execute(
            select(Payments).filter(Payments.id == payment.id),
        )
        db_payment = result.scalars().first()
        db_payment.processing_status = processing_status
        db_payment.payment_status = payment_status
        await session.commit()

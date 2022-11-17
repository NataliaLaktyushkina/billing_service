import datetime
import secrets
import string
from typing import List, Optional

from sqlalchemy import func, update
import uuid
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
            expiration_date=payment['expiration_date'],
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


async def upload_payments(processing_status: ProcessingStatus) -> List[uuid.uuid4]:
    """Choose last request from user in selected processing status"""
    async with SessionLocal() as session:
        subq = select(
            func.max(Payments.payment_date).label('payments_date'),
            Payments.user_id.label('user_id'),
        ).filter(
            Payments.processing_status == processing_status,
        ).group_by(Payments.user_id).subquery()

        result = await session.execute(
            select(Payments.id).join(
                subq, (Payments.payment_date == subq.c.payments_date) &  # noqa: W504
                      (Payments.user_id == subq.c.user_id),
            ),
        )

        return result.scalars().all()


async def mark_duplicates(original_payments=List[uuid.uuid4]):
    async with SessionLocal() as session:
        subq = select(
            Payments.user_id.label('user_id'),
        ).filter(
            Payments.id.in_(original_payments),
        ).subquery()
        result = await session.execute(
            select(Payments.id).join(
                subq, (Payments.user_id == subq.c.user_id) &  # noqa : W504
                      (Payments.id.not_in(original_payments)),
            ).filter(
                Payments.processing_status == ProcessingStatus.new,
            ),
        )
        await update_statuses(result.scalars().all(),
                              processing_status=ProcessingStatus.duplicated)


async def update_statuses(
        payment_id: List[uuid.uuid4], processing_status: ProcessingStatus,
        payment_status: PaymentStatus = PaymentStatus.unknown,
) -> None:
    async with SessionLocal() as session:
        await session.execute(
            update(
                Payments,
            ).where(
                Payments.id.in_(payment_id),
            ).values(processing_status=processing_status,
                     payment_status=payment_status),
        )
        await session.commit()


async def check_subscription(user_id: str) -> bool:
    """Check if subscription exists"""
    current_date = datetime.datetime.now()
    async with SessionLocal() as session:
        result = await session.execute(
            select(Payments).filter(
                (Payments.user_id == user_id) &  # noqa: W504
                (Payments.processing_status == ProcessingStatus.completed) &  # noqa: W504
                (Payments.payment_status == PaymentStatus.accepted) &  # noqa: W504
                (Payments.expiration_date > current_date),
            ),
        )
        if len(result.all()):
            return True
        return False

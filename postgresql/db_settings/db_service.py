import datetime
import uuid
from typing import List

from sqlalchemy import func, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from postgresql.db_settings.db import SessionLocal
from postgresql.db_settings.db_models import Payment, ProcessingStatus, PaymentStatus
from postgresql.db_settings.logger import logger


async def add_payment(payment_data: List[dict]):
    service = SessionLocal()
    for payment in payment_data:
        new_payment = Payment(
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


async def extract_new_payments() -> List[Payment]:
    async with SessionLocal() as session:
        result = await session.execute(
            select(Payment).filter(
                Payment.processing_status == ProcessingStatus.new,
            ),
        )
        return result.scalars().all()


async def upload_payments(processing_status: ProcessingStatus) -> List[uuid.uuid4]:
    """Choose last request from user in selected processing status"""
    async with SessionLocal() as session:
        subq = select(
            func.max(Payment.payment_date).label('payments_date'),
            Payment.user_id.label('user_id'),
        ).filter(
            Payment.processing_status == processing_status,
        ).group_by(Payment.user_id).subquery()

        result = await session.execute(
            select(Payment.id, Payment.user_id, Payment.subscription_type, Payment.payment_date).join(
                subq, (Payment.payment_date == subq.c.payments_date) &  # noqa: W504
                      (Payment.user_id == subq.c.user_id),
            ),
        )

        return result.all()


async def mark_duplicates(original_payments=List[uuid.uuid4]):
    async with SessionLocal() as session:
        subq = select(
            Payment.user_id.label('user_id'),
        ).filter(
            Payment.id.in_(original_payments),
        ).subquery()
        result = await session.execute(
            select(Payment.id).join(
                subq, (Payment.user_id == subq.c.user_id) &  # noqa : W504
                      (Payment.id.not_in(original_payments)),
            ).filter(
                Payment.processing_status == ProcessingStatus.new,
            ),
        )
        await update_statuses(result.scalars().all(),
                              processing_status=ProcessingStatus.duplicated)


async def update_statuses(
        payment_id: List[uuid.uuid4], processing_status: ProcessingStatus,
        payment_status: PaymentStatus = PaymentStatus.unknown,
        subscription_id: str = '',
) -> None:
    async with SessionLocal() as session:
        await session.execute(
            update(
                Payment,
            ).where(
                Payment.id.in_(payment_id),
            ).values(processing_status=processing_status,
                     payment_status=payment_status,
                     subscription_id=subscription_id),
        )
        await session.commit()


async def list_user_payments(user_id: List[str]) -> List[Payment]:
    """Check if subscription exists"""
    current_date = datetime.datetime.now()
    async with SessionLocal() as session:
        result = await session.execute(
            select(Payment).filter(
                (Payment.user_id.in_(user_id)) &  # noqa: W504
                (Payment.processing_status == ProcessingStatus.completed) &  # noqa: W504
                (Payment.payment_status == PaymentStatus.accepted) &  # noqa: W504
                (Payment.expiration_date > current_date),
            ),
        )
        return result.scalars().all()

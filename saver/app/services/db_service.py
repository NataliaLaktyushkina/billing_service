import datetime
from typing import List

from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from postgresql.db_settings.db import SessionLocal
from postgresql.db_settings.logger import logger
from postgresql.models.db_models import Payment, ProcessingStatus, PaymentStatus


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

import uuid
from typing import List

from postgresql.models.db_models import Payment, ProcessingStatus, PaymentStatus
from sqlalchemy import func, update
from sqlalchemy.future import select

from postgresql.db_settings.db import SessionLocal


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

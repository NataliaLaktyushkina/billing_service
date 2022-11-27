import datetime
from typing import List

from postgresql.models.db_models import Payment, ProcessingStatus, PaymentStatus
from sqlalchemy.future import select

from postgresql.db_settings.db import SessionLocal


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

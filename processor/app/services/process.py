import uuid
from typing import List

from core.logger import logger
from services.stripe_processing import process_payment

from postgresql.db_settings.db_models import ProcessingStatus, PaymentStatus
from postgresql.db_settings.db_service import update_statuses


async def process_payments(payments: List[uuid.uuid4]):
    await update_statuses(
        payment_id=payments,
        processing_status=ProcessingStatus.in_processing,
    )
    await send_to_processing(payments=payments)


async def send_to_processing(payments: List[uuid.uuid4]):
    for payment in payments:
        response = process_payment()
        logger.info(' '.join((response.stripe_id, response.status)))
        new_processing_status = ProcessingStatus.completed
        if response.status == 'succeeded':
            payment_status = PaymentStatus.accepted
        else:
            payment_status = PaymentStatus.error
        await update_statuses(
            payment_id=[payment],
            processing_status=new_processing_status,
            payment_status=payment_status,
        )

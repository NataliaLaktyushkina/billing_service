from typing import List

from core.logger import logger

from common.main import get_subscription_intervals
from models.payment import PaymentsShort
from postgresql.db_settings.db_models import ProcessingStatus, PaymentStatus
from postgresql.db_settings.db_service import update_statuses
from stripe_app.app.stripe_processing import process_payment


async def process_payments(payments: List[PaymentsShort]):
    payment_ids = [payment.id for payment in payments]
    await update_statuses(
        payment_id=payment_ids,
        processing_status=ProcessingStatus.in_processing,
    )
    await send_to_processing(payments=payments)


async def send_to_processing(payments: List[PaymentsShort]):
    for payment in payments:
        interval, interval_count = get_subscription_intervals(payment.subscription_type)
        response = process_payment(
            user_id=payment.user_id, email='123@mail.ru',
            interval=interval, interval_count=interval_count,
        )
        logger.info(' '.join((response.stripe_id, response.status)))
        new_processing_status = ProcessingStatus.completed
        if response.status == 'active':
            payment_status = PaymentStatus.accepted
            #  Here need to send notification letter to user via Notification service
        else:
            payment_status = PaymentStatus.error
        await update_statuses(
            payment_id=[payment.id],
            processing_status=new_processing_status,
            payment_status=payment_status,
        )

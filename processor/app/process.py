import uuid
from http import HTTPStatus
from typing import List

import requests

from core.config import settings
from core.logger import logger
from postgresql.db_settings.db_models import ProcessingStatus, PaymentStatus
from postgresql.db_settings.db_service import update_statuses


async def process_payments(payments: List[uuid.uuid4]):
    await update_statuses(
        payment_id=payments,
        processing_status=ProcessingStatus.in_processing,
    )
    await send_to_processing(payment=payments)


async def send_to_processing(payment: List[uuid.uuid4]):
    response = requests.get(
        f'{settings.PROCESSOR}/execute_transaction',
    )
    logger.info(response.content)
    new_processing_status = ProcessingStatus.processed
    if response.status_code == HTTPStatus.OK:
        payment_status = PaymentStatus.accepted
    else:
        payment_status = PaymentStatus.error
    await update_statuses(
        payment_id=payment,
        processing_status=new_processing_status,
        payment_status=payment_status,
    )

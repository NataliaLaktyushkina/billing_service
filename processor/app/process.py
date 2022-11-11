from http import HTTPStatus
from typing import List

import requests

from core.config import settings
from core.logger import logger
from postgresql.db_settings.db_models import Payments
from postgresql.db_settings.db_models import PaymentsStatus
from postgresql.db_settings.db_service import change_payment_status


async def process_payments(payments: List[Payments]):
    for payment in payments:
        await change_payment_status(
            payment=payment,
            status=PaymentsStatus.in_processing,
        )
        await send_to_processing(payment=payment)


async def send_to_processing(payment: Payments):
    response = requests.get(
        f'{settings.PROCESSOR}/execute_transaction',
    )
    logger.info(response.content)
    if response.status_code == HTTPStatus.OK:
        new_status = PaymentsStatus.processed
    else:
        new_status = PaymentsStatus.error
    await change_payment_status(payment=payment,
                                status=new_status)

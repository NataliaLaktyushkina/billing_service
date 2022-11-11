from core.logger import logger
from postgresql.db_settings.db_service import upload_payments
from postgresql.db_settings.db_models import PaymentsStatus
from postgresql.db_settings.db_service import change_payment_status


async def extract_payments() -> None:
    payments = await upload_payments(status=PaymentsStatus.to_process)
    if payments:
        logger.info(msg=payments)
        for payment in payments:
            await change_payment_status(payment=payment,
                                        status=PaymentsStatus.in_processing)

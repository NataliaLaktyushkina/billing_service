from core.logger import logger
from services.process import process_payments

from postgresql.models.db_models import ProcessingStatus
from services.db_service import mark_duplicates
from services.db_service import upload_payments


async def extract_payments() -> None:
    payments = await upload_payments(processing_status=ProcessingStatus.new)
    if payments:
        logger.info(msg=payments)
        payment_ids = [payment.id for payment in payments]
        await process_payments(payments=payments)
        await mark_duplicates(original_payments=payment_ids)

from core.logger import logger
from postgresql.db_settings.db_models import ProcessingStatus
from postgresql.db_settings.db_service import upload_payments
from process import process_payments


async def extract_payments() -> None:
    payments = await upload_payments(processing_status=ProcessingStatus.new)
    if payments:
        logger.info(msg=payments)
        await process_payments(payments=payments)

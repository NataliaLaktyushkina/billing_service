from core.config import settings
from core.logger import logger
from postgresql.db_settings.db_service import extract_new_payments
from transform import transform_payments

BATCH_SIZE = settings.BATCH_SIZE


async def extract_payments() -> None:
    new_payments = await extract_new_payments()
    logger.info(msg=new_payments)
    await transform_payments(payments=new_payments)

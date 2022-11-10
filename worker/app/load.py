from typing import List
from delete import delete_processed_payments
from postgresql.db_settings.db_models import PaymentsNew
from postgresql.db_settings.db_service import load_data_to_payments


async def load_payments(payments: List[PaymentsNew]):
    await load_data_to_payments(payments)
    await delete_processed_payments(payments=payments)

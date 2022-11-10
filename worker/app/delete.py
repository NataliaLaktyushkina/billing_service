from postgresql.db_settings.db_models import PaymentsNew
from postgresql.db_settings.db_service import delete_new_payments
from typing import List


async def delete_processed_payments(payments: List[PaymentsNew]):
    await delete_new_payments(payments)

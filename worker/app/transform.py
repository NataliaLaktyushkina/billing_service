from typing import List

from load import load_payments
from postgresql.db_settings.db_models import PaymentsNew


async def transform_payments(payments: List[PaymentsNew]):
   await load_payments(payments=payments)

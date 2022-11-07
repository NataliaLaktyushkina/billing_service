from typing import List
from delete import delete_processed_payments

async def load_payments(payments: List[dict]):
    await delete_processed_payments()

from typing import List

from load import load_payments


async def transform_payments(payments: List[dict]):
   await load_payments(payments=payments)

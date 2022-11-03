from enum import Enum

from .json_config import BaseOrjsonModel
from datetime import datetime


class PaymentStatus(str, Enum):
    new = 'new'
    in_processing = 'in processing'
    processed = 'processed'
    completed = 'completed'
    error = 'error'


class Payment(BaseOrjsonModel):
    """
      This is the description of payment model .
    """
    status: PaymentStatus
    payment_date: datetime
    payload: dict

from enum import Enum

from .json_config import BaseOrjsonModel
from datetime import datetime
from core.config import settings


class PaymentStatus(str, Enum):
    new = 'new'
    in_processing = 'in processing'
    processed = 'processed'
    completed = 'completed'
    error = 'error'


class SubscriptionId(str, Enum):
    month = 'month'
    three_months = 'three_months'
    year = 'year'


class Payment(BaseOrjsonModel):
    """
      This is the description of payment model .
    """
    payment_id: SubscriptionId  # id of supscription
    topic = settings.TOPIC_PAYMENT
    sum: int
    status: PaymentStatus
    payment_date: datetime


class PaymentAccepted(BaseOrjsonModel):
    """
      This is the description of payment model .
    """
    accepted: bool


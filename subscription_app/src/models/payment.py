import datetime
import uuid
from enum import Enum

from core.config import settings

from .json_config import BaseOrjsonModel


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


class Subscription(BaseOrjsonModel):
    id: uuid.UUID
    subscription_type: SubscriptionId
    expiration_date: datetime.datetime


class PaymentType(str, Enum):
    payment = 'payment'
    cancellation = 'cancellation'


class Payment(BaseOrjsonModel):
    """
      This is the description of payment model .
    """
    payment_id: SubscriptionId
    topic = settings.TOPIC_PAYMENT
    status: PaymentStatus
    payment_type: PaymentType


class PaymentAccepted(BaseOrjsonModel):
    """
      This is the description of payment model .
    """
    accepted: bool

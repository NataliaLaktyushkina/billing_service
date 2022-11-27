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


class SubscriptionType(str, Enum):
    month = 'month'
    three_months = 'three_months'
    year = 'year'


class UserSubscription(BaseOrjsonModel):
    id: uuid.UUID
    subscription_id: str
    subscription_type: SubscriptionType
    expiration_date: datetime.datetime


class PaymentType(str, Enum):
    payment = 'payment'


class Payment(BaseOrjsonModel):
    """
      This is the description of payment model .
    """
    subscription_type: SubscriptionType
    topic = settings.TOPIC_PAYMENT
    status: PaymentStatus
    payment_type: PaymentType


class PaymentAccepted(BaseOrjsonModel):
    """
      This is the description of payment model .
    """
    accepted: bool


class FilmAvailable(BaseOrjsonModel):
    available: bool

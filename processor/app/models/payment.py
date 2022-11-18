import datetime
import uuid
from enum import Enum

from .json_config import BaseOrjsonModel


class SubscriptionId(str, Enum):
    month = 'month'
    three_months = 'three_months'
    year = 'year'


class PaymentsShort(BaseOrjsonModel):
    id: uuid.UUID
    subscription_type: SubscriptionId
    payment_date: datetime.datetime

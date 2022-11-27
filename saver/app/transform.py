import ast
import uuid
from datetime import datetime
from typing import List

from dateutil.relativedelta import relativedelta

from postgresql.models.db_models import SubscriptionType, PaymentType
from services.db_service import add_payment
from services.db_service import list_user_payments


async def transform_data(kafka_data: List[dict]):
    processed_data = []
    for msg in kafka_data:

        data = {}
        diff = 0
        user_id, subscription_type = msg['key'].decode('utf-8').split(':')

        # check for existing subscriptions
        payments = await list_user_payments(user_id=[user_id])
        if not payments:
            data['user_id'] = uuid.UUID(user_id)
            data['subscription_type'] = SubscriptionType[subscription_type]
            value = msg['value'].decode('utf-8')
            value_dict = ast.literal_eval(value)
            data['payment_type'] = PaymentType[value_dict['payment_type']]
            payment_date = msg['timestamp'] / 1000
            data['payment_date'] = datetime.fromtimestamp(payment_date)
            if subscription_type == 'month':
                diff = relativedelta(months=1)
            elif subscription_type == 'three_months':
                diff = relativedelta(months=3)
            elif subscription_type == 'year':
                diff = relativedelta(years=1)
            data['expiration_date'] = data['payment_date'] + diff

            processed_data.append(data)

    await add_payment(processed_data)

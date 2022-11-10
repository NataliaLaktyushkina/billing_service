import uuid
import ast
from datetime import datetime
from typing import List

from postgresql.db_settings.db_service import add_payment
from postgresql.db_settings.db_models import SubscriptionTypes, PaymentsTypes


async def transform_data(kafka_data: List[dict]):
    processed_data = []
    for msg in kafka_data:

        data = {}
        user_id, subscription_type = msg['key'].decode('utf-8').split(':')
        data['user_id'] = uuid.UUID(user_id)
        data['subscription_type'] = SubscriptionTypes[subscription_type]
        value = msg['value'].decode('utf-8')
        value_dict = ast.literal_eval(value)
        data['payment_type'] = PaymentsTypes[value_dict['payment_type']]
        payment_date = int(msg['timestamp'] / 1000)
        data['payment_date'] = datetime.fromtimestamp(payment_date)

        processed_data.append(data)

    await add_payment(processed_data)

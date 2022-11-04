import uuid
import ast
from datetime import datetime
from typing import List

from database.db_service import add_payment


async def transform_data(kafka_data: List[dict]):
    processed_data = []
    for msg in kafka_data:

        data = {}
        user_id, payment_id = msg['key'].decode('utf-8').split(':')
        data['user_id'] = uuid.UUID(user_id)
        data['payment_id'] = payment_id
        value = msg['value'].decode('utf-8')
        value_dict = ast.literal_eval(value)
        data['payment_type'] = value_dict['payment_type']
        payment_date = int(msg['timestamp'] / 1000)
        data['payment_date'] = datetime.fromtimestamp(payment_date)

        processed_data.append(data)

    await add_payment(processed_data)

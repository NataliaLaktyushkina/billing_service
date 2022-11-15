from typing import Union

from fastapi import Depends
from fastapi.responses import JSONResponse

from db.kafka import get_kafka
from models.payment import PaymentAccepted, Payment
from services.service import AbstractPaymentStorage, KafkaStorage
from postgresql.db_settings.db_service import check_subscription


class PaymentHandler:
    def __init__(self, payment_storage: AbstractPaymentStorage):
        self.payment_storage = payment_storage

    async def send_payment(
            self, payment: Payment, user_id: str,
    ) -> Union[PaymentAccepted, JSONResponse]:
        subscription_exist = await check_subscription(user_id)
        if subscription_exist:
            return JSONResponse(content='Subscription is already paid')
        payment_accepted = await self.payment_storage.send_payment(payment, user_id)
        return PaymentAccepted(accepted=payment_accepted)


def get_payment_handler(
        payment_storage: AbstractPaymentStorage = Depends(get_kafka),
) -> PaymentHandler:
    return PaymentHandler(KafkaStorage(payment_storage))

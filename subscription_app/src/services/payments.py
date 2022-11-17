from typing import Union, List

from fastapi import Depends
from fastapi.responses import JSONResponse

from db.kafka import get_kafka
from models.payment import PaymentAccepted, Payment, Subscription, SubscriptionId
from services.service import AbstractPaymentStorage, KafkaStorage
from postgresql.db_settings.db_service import list_user_payments


class PaymentHandler:
    def __init__(self, payment_storage: AbstractPaymentStorage):
        self.payment_storage = payment_storage

    async def send_payment(
            self, payment: Payment, user_id: str,
    ) -> Union[PaymentAccepted, JSONResponse]:
        subscription_exist = await self.subscriptions_list(user_id)
        if len(subscription_exist):
            return JSONResponse(content='Subscription is already paid')
        payment_accepted = await self.payment_storage.send_payment(payment, user_id)
        return PaymentAccepted(accepted=payment_accepted)

    @staticmethod
    async def subscriptions_list(user_id: str) -> List[Subscription]:
        payments = await list_user_payments(user_id=user_id)
        subscription_list = []
        for payment in payments:
            subscription = Subscription(
                subscription_type=SubscriptionId[payment.subscription_type],
                expiration_date=payment.expiration_date,
            )
            subscription_list.append(subscription)
        return subscription_list






def get_payment_handler(
        payment_storage: AbstractPaymentStorage = Depends(get_kafka),
) -> PaymentHandler:
    return PaymentHandler(KafkaStorage(payment_storage))

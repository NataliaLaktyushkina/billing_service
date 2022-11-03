from fastapi import Depends
from services.service import AbstractPaymentStorage, KafkaStorage
from db.kafka import get_kafka
from models.payment import PaymentAccepted, Payment


class PaymentHandler:
    def __init__(self, payment_storage: AbstractPaymentStorage):
        self.payment_storage = payment_storage

    async def send_payment(self, payment: Payment, user_id: str) -> PaymentAccepted:
        payment_accepted = await self.payment_storage.send_payment(payment, user_id)
        return PaymentAccepted(accepted=payment_accepted)


def get_payment_handler(
        payment_storage: AbstractPaymentStorage = Depends(get_kafka)
) -> PaymentHandler:
    return PaymentHandler(KafkaStorage(payment_storage))

from typing import Union, List

from fastapi import Depends
from fastapi.responses import JSONResponse

from db.kafka import get_kafka
from models.payment import PaymentAccepted, Payment, UserSubscription, SubscriptionType
from models.payment import FilmAvailable
from services.service import AbstractPaymentStorage, KafkaStorage
from postgresql.db_settings.db_service import list_user_payments
from services.movie_data import check_movie_subscription


class PaymentHandler:
    def __init__(self, payment_storage: AbstractPaymentStorage):
        self.payment_storage = payment_storage

    async def send_payment(
            self, payment: Payment, user_id: str,
    ) -> Union[PaymentAccepted, JSONResponse]:
        payment_accepted = await self.payment_storage.send_payment(payment, user_id)
        return PaymentAccepted(accepted=payment_accepted)

    @staticmethod
    async def subscriptions_list(user_id: str) -> List[UserSubscription]:
        payments = await list_user_payments(user_id=[user_id])
        subscription_list = []
        for payment in payments:
            subscription = UserSubscription(
                id=payment.id,
                subscription_id=payment.subscription_id,
                subscription_type=SubscriptionType[payment.subscription_type],
                expiration_date=payment.expiration_date,
            )
            subscription_list.append(subscription)
        return subscription_list

    async def check_availability(
            self, user_id: str,
            film_id: str,
    ) -> FilmAvailable:
        # check subscription
        user_subscriptions = await self.subscriptions_list(user_id)
        # check if film by subscription in movie service
        film_by_subscription = check_movie_subscription(film_id=film_id)
        available = True
        if film_by_subscription and len(user_subscriptions) == 0:
            available = False
        return FilmAvailable(available=available)


def get_payment_handler(
        payment_storage: AbstractPaymentStorage = Depends(get_kafka),
) -> PaymentHandler:
    return PaymentHandler(KafkaStorage(payment_storage))

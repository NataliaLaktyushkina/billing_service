import datetime
from typing import List

from core.logger import logger
from services.stripe_processing import process_payment

from models.payment import PaymentsShort
from postgresql.db_settings.db_models import ProcessingStatus, PaymentStatus, SubscriptionTypes
from postgresql.db_settings.db_service import update_statuses
from postgresql.db_settings.db_service_admin import get_subscriptions_cost


async def process_payments(payments: List[PaymentsShort]):
    payment_ids = [payment.id for payment in payments]
    await update_statuses(
        payment_id=payment_ids,
        processing_status=ProcessingStatus.in_processing,
    )
    await send_to_processing(payments=payments)


async def get_payment_cost(
        cost_date: datetime.date,
        subscription_type: SubscriptionTypes) -> int:
    costs = await get_subscriptions_cost(
        cost_date=cost_date,
    )
    payment_cost = [cost.cost
                 for cost in costs
                 if cost.subscription_type == subscription_type]
    if payment_cost:
        return payment_cost[0]
    return 0


async def send_to_processing(payments: List[PaymentsShort]):
    for payment in payments:
        payment_cost = await get_payment_cost(
            cost_date=payment.payment_date,
            subscription_type=payment.subscription_type,
        )
        if payment_cost:
            response = process_payment(amount=payment_cost*100)
            logger.info(' '.join((response.stripe_id, response.status)))
            new_processing_status = ProcessingStatus.completed
            if response.status == 'succeeded':
                payment_status = PaymentStatus.accepted
            else:
                payment_status = PaymentStatus.error
            await update_statuses(
                payment_id=[payment.id],
                processing_status=new_processing_status,
                payment_status=payment_status,
            )
        else:
            logger.error('Cost must be greater than 0')

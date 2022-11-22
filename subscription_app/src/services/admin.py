import datetime
from typing import Union, List

from fastapi.responses import JSONResponse
from stripe.error import InvalidRequestError

from models.admin import CostUpdated, SubscriptionCost
from models.payment import UserSubscription, SubscriptionId
from postgresql.db_settings.db_service import list_user_payments
from postgresql.db_settings.db_service_admin import change_subscription_cost
from postgresql.db_settings.db_service_admin import get_subscriptions_cost
from postgresql.db_settings.db_service_admin import get_users_list
from stripe_app.app.stripe_processing import update_or_create_price


async def change_cost_subscription(
        name: str,
        new_cost: int,
        starting_date: datetime.date,
) -> Union[CostUpdated, JSONResponse]:

    interval, interval_count = get_subscription_intervals(name)

    try:
        cost_updated = await change_subscription_cost(
            subscription_type=name,
            cost=new_cost,
            starting_date=starting_date,
        )
        if cost_updated:
            update_or_create_price(new_cost, interval, interval_count)

        return CostUpdated(updated=cost_updated)
    except InvalidRequestError as e:
        return JSONResponse(content=e.user_message)


def get_subscription_intervals(subscription_name: str) -> tuple:
    if subscription_name=='month':
        interval = 'month'
        interval_count = 1
    elif subscription_name == 'three_months':
        interval = 'month'
        interval_count = 3
    elif subscription_name == 'year':
        interval = 'year'
        interval_count = 1
    return interval, interval_count


async def subscriptions_cost(cost_date: datetime.date) -> List[SubscriptionCost]:
    list_costs = await get_subscriptions_cost(cost_date=cost_date)
    return [SubscriptionCost(subscription=lc.subscription_type,
                             cost=lc.cost) for lc in list_costs]


async def users_subscriptions() -> List[UserSubscription]:
    users = await get_users_list()
    subscriptions = await list_user_payments(user_id=users)
    return [UserSubscription(
                user_id=subscription.user_id,
                id=subscription.id,
                subscription_type=SubscriptionId[subscription.subscription_type],
                expiration_date=subscription.expiration_date,
            ) for subscription in subscriptions]

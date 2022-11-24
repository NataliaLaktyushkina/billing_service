import datetime
from typing import Union, List

from fastapi.responses import JSONResponse

from common.main import get_subscription_intervals
from models.admin import CostUpdated, SubscriptionCost, SubscriptionDeleted
from models.payment import UserSubscription, SubscriptionId
from postgresql.db_settings.db_service import list_user_payments
from postgresql.db_settings.db_service_admin import change_subscription_cost
from postgresql.db_settings.db_service_admin import get_subscriptions_cost
from postgresql.db_settings.db_service_admin import get_users_list
from postgresql.db_settings.db_service_admin import stop_subscription
from stripe_app.app.stripe_processing import delete_subscription
from stripe_app.app.stripe_processing import update_or_create_price


async def change_cost_subscription(
        name: str,
        new_cost: int,
        starting_date: datetime.date,
) -> Union[CostUpdated, JSONResponse]:
    interval, interval_count = get_subscription_intervals(name)
    resp = update_or_create_price(new_cost, interval, interval_count)
    if resp.active:
        cost_updated = await change_subscription_cost(
            subscription_type=name,
            cost=new_cost,
            starting_date=starting_date,
        )

    return CostUpdated(updated=cost_updated)


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


async def cancel_subscription(subscription_id: str) -> SubscriptionDeleted:
    resp = delete_subscription(subscription_id)
    stopped = False
    if resp.status == 'canceled':
        stopped = await stop_subscription([subscription_id])
    return SubscriptionDeleted(deleted=stopped)

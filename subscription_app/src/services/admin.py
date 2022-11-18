import datetime
from typing import Union, List

from fastapi.responses import JSONResponse

from models.admin import CostUpdated, SubscriptionCost
from models.payment import UserSubscription, SubscriptionId
from postgresql.db_settings.db_service_admin import change_subscription_cost
from postgresql.db_settings.db_service_admin import get_subscriptions_cost
from postgresql.db_settings.db_service_admin import get_users_list
from postgresql.db_settings.db_service import list_user_payments


async def change_cost_subscription(
        name: str,
        new_cost: int,
        starting_date: datetime.date,
) -> Union[CostUpdated, JSONResponse]:
    cost_updated = await change_subscription_cost(
        subscription_type=name,
        cost=new_cost,
        starting_date=starting_date,
    )
    if cost_updated:
        return CostUpdated(updated=cost_updated)
    else:
        return JSONResponse(content='Check date and subscription type')


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

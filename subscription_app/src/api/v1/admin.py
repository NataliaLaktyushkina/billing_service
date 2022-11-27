from datetime import date
from typing import List

from fastapi import APIRouter, Depends, Query

from models.admin import CostUpdated, SubscriptionCost, SubscriptionDeleted
from models.payment import SubscriptionType, UserSubscription
from services.admin import cancel_subscription
from services.admin import change_cost_subscription, subscriptions_cost, users_subscriptions
from services.jwt_check import JWTBearer

router = APIRouter()


@router.post('/', description='Update cost of subscription',
             response_model=CostUpdated,
             response_description='Cost of subscription was updated')
async def update_subscription_cost(
        name: SubscriptionType,
        new_cost: int,
        starting_date: date = Query(default=date.today()),
        user_id: str = Depends(JWTBearer()),
) -> CostUpdated:
    return await change_cost_subscription(
        name=name,
        new_cost=new_cost,
        starting_date=starting_date,
    )


@router.get('/', description='List of subscriptions with cost',
            response_model=List[SubscriptionCost],
            response_description='List of subscriptions with cost')
async def get_subscriptions_cost(
        cost_date: date = Query(default=date.today()),
        user_id: str = Depends(JWTBearer()),
) -> List[SubscriptionCost]:
    return await subscriptions_cost(cost_date=cost_date)


@router.get('/users/', description='List of users subscriptions',
            response_model=List[UserSubscription],
            response_description='List of users subscriptions')
async def get_users_subscriptions(
        user_id: str = Depends(JWTBearer()),
) -> List[UserSubscription]:
    return await users_subscriptions()


@router.delete('/', description='Delete subscription',
               response_model=SubscriptionDeleted,
               response_description='Subscription was successfully cancelled')
async def stop_subscription(
        subscription_id: str,
        user_id: str = Depends(JWTBearer()),
) -> SubscriptionDeleted:
    return await cancel_subscription(
        subscription_id=subscription_id,
    )

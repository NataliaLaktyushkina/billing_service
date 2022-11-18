from datetime import date

from fastapi import APIRouter, Depends, Query

from models.admin import CostUpdated
from models.payment import SubscriptionId
from services.admin import change_cost_subscription
from services.jwt_check import JWTBearer

router = APIRouter()


@router.post('/', description='Update cost of subscription',
             response_model=CostUpdated,
             response_description='Cost of subscription was updated')
async def update_subscription_cost(
        name: SubscriptionId,
        new_cost: int,
        starting_date: date = Query(default=date.today()),
        user_id: str = Depends(JWTBearer()),
) -> CostUpdated:
    return await change_cost_subscription(
        name=name,
        new_cost=new_cost,
        starting_date=starting_date,
    )

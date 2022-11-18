import datetime

from models.admin import CostUpdated
from postgresql.db_settings.db_service_admin import change_subscription_cost
from fastapi.responses import JSONResponse

from typing import Union


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

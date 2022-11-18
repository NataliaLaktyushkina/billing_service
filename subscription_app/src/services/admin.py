import datetime

from models.admin import CostUpdated
from postgresql.db_settings.db_service_admin import change_subscription_cost


async def change_cost_subscription(
        name: str,
        new_cost: int,
        starting_date: datetime.date,
) -> CostUpdated:
    await change_subscription_cost(
        subscription_type=name,
        cost=new_cost,
        starting_date=starting_date,
    )
    return CostUpdated(updated=True)

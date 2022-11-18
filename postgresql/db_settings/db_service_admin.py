import datetime

from sqlalchemy.exc import IntegrityError

from postgresql.db_settings.db import SessionLocal
from postgresql.db_settings.db_models import SubscriptionCost, SubscriptionTypes
from postgresql.db_settings.logger import logger


async def change_subscription_cost(
        subscription_type: str,
        cost: int,
        starting_date: datetime.date,
):
    service = SessionLocal()

    new_cost = SubscriptionCost(
        subscription_type=SubscriptionTypes[subscription_type],
        cost=cost,
        creation_date=starting_date,
    )

    service.add(new_cost)
    try:
        await service.commit()
        return True
    except IntegrityError:
        logger.error(msg='Check date and subscription type')

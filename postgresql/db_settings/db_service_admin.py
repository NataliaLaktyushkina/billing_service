import datetime
from typing import List

from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy import func

from postgresql.db_settings.db import SessionLocal
from postgresql.db_settings.db_models import SubscriptionCost, SubscriptionTypes, User
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


async def get_subscriptions_cost(
        cost_date: datetime.date,
) -> List[SubscriptionCost]:
    async with SessionLocal() as session:
        today = datetime.date.today()

        subq = select(
            func.max(SubscriptionCost.creation_date).label('creation_date'),
            SubscriptionCost.subscription_type.label('subscription'),
        ).filter(
            (SubscriptionCost.creation_date <= cost_date) &  # noqa: W504
            (SubscriptionCost.creation_date <= today),
        ).group_by(SubscriptionCost.subscription_type).subquery()

        result = await session.execute(
            select(SubscriptionCost).join(
                subq, (SubscriptionCost.subscription_type == subq.c.subscription) &  # noqa: W504
                      (SubscriptionCost.creation_date == subq.c.creation_date),
            ),
        )
        return result.scalars().all()


async def get_users_list() -> List[str]:
    async with SessionLocal() as session:
        result = await session.execute(
            select(User.id),
        )
        return result.scalars().all()

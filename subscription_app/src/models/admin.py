from .json_config import BaseOrjsonModel


class SubscriptionCost(BaseOrjsonModel):
    subscription: str
    cost: int


class CostUpdated(BaseOrjsonModel):
    updated: bool

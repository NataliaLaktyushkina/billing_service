from .json_config import BaseOrjsonModel


class Subscription(BaseOrjsonModel):
    name: str


class SubscriptionCost(BaseOrjsonModel):
    subscription: Subscription
    cost: int


class CostUpdated(BaseOrjsonModel):
    updated: bool

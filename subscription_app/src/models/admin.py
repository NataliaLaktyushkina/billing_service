from .json_config import BaseOrjsonModel


class SubscriptionDeleted(BaseOrjsonModel):
    """
      This is the description of payment model .
    """
    deleted: bool


class SubscriptionCost(BaseOrjsonModel):
    subscription: str
    cost: int


class CostUpdated(BaseOrjsonModel):
    updated: bool

from enum import Enum


class SubscriptionInterval(Enum):
    ANNUAL = 'ANNUAL'
    EVERY_30_DAYS = 'EVERY_30_DAYS'


class SubscriptionStatus(Enum):
    ACTIVE = 'ACTIVE'
    CANCELLED = 'CANCELLED'


class SubscriptionType(Enum):
    APP_SUBSCRIPTION = 'AppSubscription'

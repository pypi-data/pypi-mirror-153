import dataclasses

from shopify_client.billing.schema.requests.plan import Plan


@dataclasses.dataclass
class AppSubscriptionLineItem:
    plan: Plan

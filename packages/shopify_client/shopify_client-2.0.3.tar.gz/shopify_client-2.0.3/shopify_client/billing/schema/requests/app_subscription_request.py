import dataclasses

from shopify_client.billing.schema.requests.base_charge_request import BaseChargeRequest
from shopify_client.billing.schema.requests.line_item import AppSubscriptionLineItem


@dataclasses.dataclass
class AppSubscriptionRequest(BaseChargeRequest):
    lineItems: [AppSubscriptionLineItem]
    trialDays: int = 0
    test: bool = False

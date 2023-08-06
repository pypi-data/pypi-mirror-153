import dataclasses

from shopify_client.billing.schema.requests.base_charge_request import BaseChargeRequest
from shopify_client.billing.schema.requests.price import Price


@dataclasses.dataclass
class OneTimePurchaseRequest(BaseChargeRequest):
    price: Price
    test: bool = False

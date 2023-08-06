import dataclasses

from shopify_client.common.schema.response import UserError
from .webhook_subscription import WebhookSubscription


@dataclasses.dataclass
class SubscriptionResponse:
    subscription: WebhookSubscription
    user_errors: [UserError] = None

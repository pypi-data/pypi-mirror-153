import dataclasses

from shopify_client.common.schema.response import UserError


@dataclasses.dataclass
class SubscriptionDeleteResponse:
    deleted_webhook_subscription_id: str
    user_error: UserError = None

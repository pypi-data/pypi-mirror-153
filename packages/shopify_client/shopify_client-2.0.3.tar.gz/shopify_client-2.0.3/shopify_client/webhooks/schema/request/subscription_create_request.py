import dataclasses

from .subscription_input import WebhookSubscriptionInput


@dataclasses.dataclass
class WebhookSubscriptionCreateRequest:
    topic: str
    webhook_subscription: WebhookSubscriptionInput

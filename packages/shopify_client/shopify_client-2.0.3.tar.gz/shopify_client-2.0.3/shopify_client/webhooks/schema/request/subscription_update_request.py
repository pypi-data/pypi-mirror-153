import dataclasses

from .subscription_input import WebhookSubscriptionInput


@dataclasses.dataclass
class WebhookSubscriptionUpdateRequest:
    id: str
    webhook_subscription: WebhookSubscriptionInput

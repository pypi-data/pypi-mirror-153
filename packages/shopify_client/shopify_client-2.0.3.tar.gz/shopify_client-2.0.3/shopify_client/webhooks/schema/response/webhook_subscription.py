import dataclasses


@dataclasses.dataclass
class WebhookSubscription:
    id: str
    callback_url: str
    topic: str
    created_at: str
    updated_at: str

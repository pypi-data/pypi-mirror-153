from typing import Optional

from shopify_client.webhooks.schema.response import WebhookSubscription


class SubscriptionParseMixin:
    def parse_subscription(self, response) -> Optional[WebhookSubscription]:
        if not response:
            return

        return WebhookSubscription(
            id=response['id'],
            callback_url=response['endpoint']['callbackUrl'],
            topic=response['topic'],
            created_at=response['createdAt'],
            updated_at=response['updatedAt']
        )

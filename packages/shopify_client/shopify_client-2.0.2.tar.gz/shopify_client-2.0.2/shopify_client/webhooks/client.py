from shopify_client import base_client
from .schema.response import SubscriptionResponse, SubscriptionDeleteResponse
from .subscriptions import WebhookSubscriptionCreate, WebhookSubscriptionDelete, WebhookSubscriptionUpdate


class WebhookClient(base_client.BaseClient):
    def create(self, request) -> SubscriptionResponse:
        return WebhookSubscriptionCreate().create(request)

    def update(self, request) -> SubscriptionResponse:
        return WebhookSubscriptionUpdate().update(request)

    def delete(self, request) -> SubscriptionDeleteResponse:
        return WebhookSubscriptionDelete().delete(request)

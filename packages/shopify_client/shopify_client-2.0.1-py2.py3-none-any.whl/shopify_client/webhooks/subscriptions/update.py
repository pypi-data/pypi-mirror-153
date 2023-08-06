from shopify_client.common.mixins import UserErrorParserMixin
from .base import BaseWebhookSubscription
from ..mixins import SubscriptionParseMixin
from ..schema.request import WebhookSubscriptionUpdateRequest
from ..schema.response import SubscriptionResponse


class WebhookSubscriptionUpdate(BaseWebhookSubscription, SubscriptionParseMixin, UserErrorParserMixin):
    def update(self, request: WebhookSubscriptionUpdateRequest):
        return self.execute(request)

    def generate_mutation(self) -> str:
        return '''
            fragment endpointObject on WebhookHttpEndpoint {
                callbackUrl
            }

            mutation webhookSubscriptionUpdate($id: ID!, $webhookSubscription: WebhookSubscriptionInput!) {
                webhookSubscriptionUpdate(
                    id: $id
                    webhookSubscription: $webhookSubscription
                ) {
                    userErrors {
                        field
                        message
                    }
                    webhookSubscription {
                        id
                        createdAt
                        endpoint {
                            ...endpointObject
                        }
                        topic
                        updatedAt
                    }
                }
            }
        '''

    def get_variables(self, request: WebhookSubscriptionUpdateRequest) -> dict:
        return {
            'id': request.id,
            'webhookSubscription': {
                'callbackUrl': request.webhook_subscription.callback_url,
                'includeFields': request.webhook_subscription.include_fields,
                'metafieldNamespaces': request.webhook_subscription.metafield_namespaces,
                'format': request.webhook_subscription.format,
            }
        }

    def parse_response(self, response):
        response_object = response['data']['webhookSubscriptionUpdate']

        return SubscriptionResponse(
            subscription=self.parse_subscription(response_object['webhookSubscription']),
            user_errors=self.parse_user_error(response_object['userErrors'])
        )

from shopify_client.common.mixins import UserErrorParserMixin
from .base import BaseWebhookSubscription
from ..schema.request import WebhookSubscriptionDeleteRequest
from ..schema.response import SubscriptionDeleteResponse


class WebhookSubscriptionDelete(BaseWebhookSubscription, UserErrorParserMixin):
    def delete(self, request: WebhookSubscriptionDeleteRequest):
        return self.execute(request)

    def generate_mutation(self) -> str:
        return '''
            mutation webhookSubscriptionDelete($id: ID!) {
                webhookSubscriptionDelete(id: $id) {
                    userErrors {
                        field
                        message
                    }
                    deletedWebhookSubscriptionId
                }
            }
        '''

    def get_variables(self, request: WebhookSubscriptionDeleteRequest) -> dict:
        return {
            'id': request.id,
        }

    def parse_response(self, response):
        if not response:
            return

        subscription_delete_response = response['data']['webhookSubscriptionDelete']
        return SubscriptionDeleteResponse(
            deleted_webhook_subscription_id=subscription_delete_response['deletedWebhookSubscriptionId'],
            user_error=self.parse_user_error(subscription_delete_response['userErrors'])
        )

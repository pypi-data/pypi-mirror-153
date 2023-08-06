import json

import shopify

from shopify_client.billing.charges.base_charge import BaseCharge
from shopify_client.billing.constants import SubscriptionType, SubscriptionStatus
from shopify_client.billing.schema.objects import AppSubscriptionObject


class AppSubscription(BaseCharge):
    @property
    def charge_type(self):
        return 'appSubscription'

    @property
    def variable_type_string(self):
        return (
            "$name: String!, $lineItems: [AppSubscriptionLineItemInput!]!, $returnUrl: URL!, $trialDays: Int!, "
            "$test: Boolean!"
        )

    @property
    def variable_string(self):
        return "name: $name, lineItems: $lineItems, returnUrl: $returnUrl, trialDays: $trialDays, test: $test"

    @property
    def charge_resource(self):
        return shopify.RecurringApplicationCharge

    # Active Subscription Specific Code
    @property
    def active_subscription(self):
        response = shopify.GraphQL().execute(query=self.active_subscription_query)
        return self.parse_active_subscription(json.loads(response))

    @property
    def active_subscription_query(self):
        return '''
            {
                appInstallation {
                    activeSubscriptions {
                        id
                        name
                        status
                        __typename
                    }
                }
            }
        '''

    def parse_active_subscription(self, response):
        active_subscription = next(
            (
                subscription for subscription in response['data']['appInstallation']['activeSubscriptions']
                if self.is_valid_subscription(subscription)
            ),
            None
        )

        if not active_subscription:
            return

        active_subscription.pop('__typename', None)
        return AppSubscriptionObject(**active_subscription)

    def is_valid_subscription(self, subscription):
        return (
                subscription['__typename'] == SubscriptionType.APP_SUBSCRIPTION.value and
                subscription['status'] == SubscriptionStatus.ACTIVE.value
        )

    # Cancellation Specific Code
    def cancel_active_subscription(self):
        active_subscription = self.active_subscription
        if not active_subscription:
            return

        response = shopify.GraphQL().execute(
            query=self.cancel_mutation, variables=self.cancel_variables(active_subscription)
        )
        return self.parse_cancel_subscription(json.loads(response))

    @property
    def cancel_mutation(self):
        return '''
            mutation appSubscriptionCancel($id: ID!) {
                appSubscriptionCancel(id: $id) {
                    appSubscription {
                        id
                        name
                        status
                    }
                    userErrors {
                        field
                        message
                    }
                }
            }
        '''

    def cancel_variables(self, subscription: AppSubscriptionObject):
        return {
            'id': subscription.id
        }

    def parse_cancel_subscription(self, response):
        return AppSubscriptionObject(**response['data']['appSubscriptionCancel']['appSubscription'])

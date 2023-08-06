from shopify_client.base_client import BaseClient
from shopify_client.billing.charges import OneTimePurchase, AppSubscription


class BillingClient(BaseClient):
    @property
    def one_time_purchase(self):
        return OneTimePurchase()

    @property
    def app_subscription(self):
        return AppSubscription()

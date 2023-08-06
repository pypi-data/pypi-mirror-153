from shopify_client.base_client import BaseClient
from shopify_client.store_properties.shop import ShopClient


class StorePropertiesClient(BaseClient):
    @property
    def shop(self):
        return ShopClient()

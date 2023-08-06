from shopify_client.store_properties.shop.get import ShopGet


class ShopClient:
    def get(self):
        return ShopGet().get()

from .get import ProductGet
from .metafields import MetafieldClient
from .update import ProductUpdate
from .variants import VariantClient


class ProductClient:
    @staticmethod
    def get(products_input):
        return ProductGet().get(products_input)

    @staticmethod
    def update(product_input):
        return ProductUpdate().get(product_input)

    @property
    def metafields(self):
        return MetafieldClient

    @property
    def variants(self):
        return VariantClient

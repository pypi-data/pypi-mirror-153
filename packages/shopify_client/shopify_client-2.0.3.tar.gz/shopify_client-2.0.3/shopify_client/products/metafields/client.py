from .create import MetafieldsCreate
from .update import MetafieldsUpdate


class MetafieldClient:
    @staticmethod
    def create(product_metafields_input):
        return MetafieldsCreate().create(product_metafields_input)

    @staticmethod
    def update(product_metafields_update_input):
        return MetafieldsUpdate().update(product_metafields_update_input)

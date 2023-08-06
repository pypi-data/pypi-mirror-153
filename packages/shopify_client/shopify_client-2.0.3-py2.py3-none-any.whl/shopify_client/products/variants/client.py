from .get_single import VariantsGetSingle
from .update import VariantsUpdate


class VariantClient:
    @staticmethod
    def get_single(variant_input):
        return VariantsGetSingle().get(variant_input)

    @staticmethod
    def update(variant_update_input):
        return VariantsUpdate().update(variant_update_input)

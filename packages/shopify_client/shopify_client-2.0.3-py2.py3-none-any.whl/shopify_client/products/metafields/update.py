import shopify

from .utils import MetafieldMixin
from ..schema import ProductMetafieldUpdateInput


class MetafieldsUpdate(MetafieldMixin):
    def update(self, product_metafield_update_input):
        response = shopify.GraphQL().execute(
            self.generate_mutation(), self.get_variables(product_metafield_update_input)
        )
        return self.parse_response(response)

    def generate_mutation(self):
        return """
            mutation($input: ProductInput!, $namespace: String){
                productUpdate(input: $input){
                    product {
                        metafields(namespace: $namespace, first: 100) {
                            edges {
                                node {
                                    id
                                    namespace
                                    key
                                    value
                                }
                            }
                        }
                    }
                }
            }
        """

    def get_variables(self, product_metafield_input: ProductMetafieldUpdateInput):
        metafields = [
            {
                'id': metafield.id,
                'value': metafield.value,
            } for metafield in product_metafield_input.metafields
        ]

        return {
            "input": {
                "id": product_metafield_input.product_id,
                "metafields": metafields
            },
            "namespace": product_metafield_input.namespace
        }

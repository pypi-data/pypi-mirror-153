import shopify

from .utils import MetafieldMixin
from ..schema import ProductMetafieldInput


class MetafieldsCreate(MetafieldMixin):
    def create(self, product_metafield_input):
        response = shopify.GraphQL().execute(self.generate_mutation(), self.get_variables(product_metafield_input))
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

    def get_variables(self, product_metafield_input: ProductMetafieldInput):
        metafields = [
            {
                'namespace': metafield.namespace,
                'key': metafield.key,
                'value': metafield.value,
                'type': metafield.data_type
            } for metafield in product_metafield_input.metafields
        ]

        return {
            "input": {
                "id": product_metafield_input.product_id,
                "metafields": metafields
            },
            "namespace": product_metafield_input.metafields[0].namespace
        }

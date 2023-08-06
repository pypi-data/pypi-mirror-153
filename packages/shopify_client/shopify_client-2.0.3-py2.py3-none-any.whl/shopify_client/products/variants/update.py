import json

import shopify

from shopify_client.common.mixins import UserErrorParserMixin


class VariantsUpdate(UserErrorParserMixin):
    def update(self, variant_update_input):
        response = shopify.GraphQL().execute(self.get_query(), self.get_variables(variant_update_input))
        return self.get_parsed_response(json.loads(response))

    def get_query(self):
        return '''
            mutation productVariantUpdate($input: ProductVariantInput!) {
                productVariantUpdate(input: $input) {
                    product {
                        title
                        handle
                        status
                    }
                    productVariant {
                        id
                        displayName
                        price
                        sku
                        availableForSale
                    }
                    userErrors {
                        field
                        message
                    }
                }
            }
        '''

    def get_variables(self, variant_update_input):
        variant_id = variant_update_input.pop('variant_id')
        return {
            'input': {
                'id': variant_id,
                **variant_update_input
            }
        }

    def get_parsed_response(self, response):
        response_data = response['data']['productVariantUpdate']
        return {
            'product': response_data['product'],
            'variant': response_data['productVariant'],
            'user_errors': self.parse_user_error(response_data['userErrors'])
        }

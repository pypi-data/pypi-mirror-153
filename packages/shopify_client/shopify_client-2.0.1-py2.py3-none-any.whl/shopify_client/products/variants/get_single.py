import json

import shopify


class VariantsGetSingle:
    def get(self, variant_input):
        response = shopify.GraphQL().execute(self.get_query(), self.get_variables(variant_input))
        return self.get_parse_response(json.loads(response))

    def get_query(self):
        return '''
            query getVariant($id: ID!){
                productVariant(id: $id){
                    id
                    title
                    displayName
                    price
                    sku
                    availableForSale
                }
            }
        '''

    def get_variables(self, variants_input):
        return {
            'id': variants_input['variant_id']
        }

    def get_parse_response(self, response):
        return response['data']['productVariant']

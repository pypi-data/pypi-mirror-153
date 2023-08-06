import shopify

from shopify_client.common.mixins import UserErrorParserMixin


class ProductUpdate(UserErrorParserMixin):
    def get(self, product_input):
        response = shopify.GraphQL().execute(self.get_query(), self.get_variables(product_input))
        return response

    def get_query(self):
        return '''
            mutation productUpdate($input: ProductInput!){
                productUpdate(input: $input){
                    product {
                        id
                        title
                        handle
                        status
                    }
                    userErrors {
                      field
                      message
                    }
                }   
            }
        '''

    def get_variables(self, product_input):
        product_id = product_input.pop('id')
        return {
            'input': {
                'id': product_id,
                **product_input
            }
        }

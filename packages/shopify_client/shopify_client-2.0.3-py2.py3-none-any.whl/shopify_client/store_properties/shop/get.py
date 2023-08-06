import json

import shopify


class ShopGet:
    def get(self):
        response = shopify.GraphQL().execute(self.get_query())
        return self.parse_response(json.loads(response))

    def get_query(self):
        return '''
            query Shop {
                shop {
                    name
                    email
                    currencyCode
                    plan {
                        displayName
                        shopifyPlus
                        partnerDevelopment
                    }
                }
            }
        '''

    def parse_response(self, response):
        shop = response.get('data', {}).get('shop')
        if not shop:
            return

        plan = shop['plan']

        return {
            'name': shop['name'],
            'email': shop['email'],
            'currency_code': shop['currencyCode'],
            'plan': {
                'name': plan['displayName'],
                'is_shopify_plus': plan['shopifyPlus'],
                'is_partner_development': plan['partnerDevelopment']
            }
        }

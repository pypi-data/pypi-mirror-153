from shopify_client.common.graphql_client import GraphqlClient
from shopify_client.common.mixins import UserErrorParserMixin


class BulkOrdersGet(GraphqlClient, UserErrorParserMixin):
    def get_query(self):
        return '''
            mutation GetBulkOrders {
                bulkOperationRunQuery(
                    query: """
                        {
                            orders {
                                edges {
                                    node {
                                        id
                                        createdAt
                                        lineItems {
                                            edges {
                                                node {
                                                    originalTotalSet {
                                                        shopMoney {
                                                            amount
                                                        }
                                                    }
                                                    quantity
                                                    variant {
                                                        id
                                                        product {
                                                            id
                                                        }
                                                        price
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                """
                ) {
                    bulkOperation {
                        id
                        status
                    }
                    userErrors {
                        field
                        message
                    }
                }
            }
        '''

    def get_variables(self, operation_input):
        return None

    def get_parsed_response(self, response):
        response_data = response['data']['bulkOperationRunQuery']
        return {
            'operation_id': response_data.get('bulkOperation').get('id'),
            'status': response_data.get('bulkOperation').get('status'),
            'user_errors': self.parse_user_error(response_data['userErrors'])
        }

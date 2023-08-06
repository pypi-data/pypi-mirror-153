from shopify_client.common.graphql_client import GraphqlClient


class BulkOperationGet(GraphqlClient):
    def get_query(self):
        return '''
           query GetBulkOperationResult($operationId: ID!){
                node(id: $operationId){
                    ... on BulkOperation {
                        id
                        status
                        url
                        partialDataUrl
                        errorCode
                        fileSize
                        objectCount
                        createdAt
                        completedAt
                    }
                }
            }
        '''

    def get_variables(self, operation_input):
        return {
            'operationId': operation_input['id']
        }

    def get_parsed_response(self, response):
        response_data = response['data']['node']

        return {
            'id': response_data['id'],
            'data_url': response_data['url'],
            'error_code': response_data['errorCode'],
            'file_size': response_data['fileSize'],
            'object_count': response_data['objectCount']
        }

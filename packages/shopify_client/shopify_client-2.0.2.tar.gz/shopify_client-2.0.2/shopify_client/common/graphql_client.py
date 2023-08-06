import abc
import json

import shopify


class GraphqlClient(abc.ABC):
    def execute(self, operation_input=None):
        response = shopify.GraphQL().execute(self.get_query(), self.get_variables(operation_input))
        return self.get_parsed_response(json.loads(response))

    @abc.abstractmethod
    def get_query(self):
        raise NotImplemented()

    @abc.abstractmethod
    def get_variables(self, operation_input):
        raise NotImplemented()

    def get_parsed_response(self, response):
        return response

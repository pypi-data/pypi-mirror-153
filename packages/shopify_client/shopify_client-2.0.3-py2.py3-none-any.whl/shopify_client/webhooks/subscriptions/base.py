import abc
import json

import shopify


class BaseWebhookSubscription(abc.ABC):
    def execute(self, *args, **kwargs):
        response = shopify.GraphQL().execute(self.generate_mutation(), self.get_variables(*args, **kwargs))
        return self.parse_response(json.loads(response))

    @abc.abstractmethod
    def generate_mutation(self) -> str:
        raise NotImplemented()

    def get_variables(self, *args, **kwargs) -> dict:
        raise NotImplemented()

    def parse_response(self, response):
        raise NotImplemented()

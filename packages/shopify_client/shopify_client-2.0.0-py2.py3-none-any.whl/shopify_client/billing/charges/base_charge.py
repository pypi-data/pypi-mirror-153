import abc
import dataclasses
import json

import shopify

from shopify_client.billing.schema import BaseChargeRequest, ChargeCreateResponse


class BaseCharge(abc.ABC):
    @property
    @abc.abstractmethod
    def charge_type(self):
        raise NotImplemented()

    @property
    @abc.abstractmethod
    def variable_type_string(self):
        raise NotImplemented()

    @property
    @abc.abstractmethod
    def variable_string(self):
        raise NotImplemented()

    @property
    @abc.abstractmethod
    def charge_resource(self):
        raise NotImplemented()

    def create(self, charge_request: BaseChargeRequest) -> ChargeCreateResponse:
        response = shopify.GraphQL().execute(self.generate_mutation(), self.get_variables(charge_request))
        return self.parse_response(json.loads(response))

    def get(self, charge_id: int):
        return self.charge_resource.find(charge_id)

    def generate_mutation(self) -> str:
        return """
            mutation %sCreate(%s) {
                %sCreate(%s) {
                    %s
                    %s
                }
            }
        """ % (
            self.charge_type, self.variable_type_string,
            self.charge_type, self.variable_string,
            self.specific_fields(), self.common_fields()
        )

    def get_variables(self, charge_request: BaseChargeRequest) -> dict:
        return dataclasses.asdict(charge_request)

    def parse_response(self, response: dict) -> ChargeCreateResponse:
        charge_data = response['data'][f'{self.charge_type}Create']

        charge_info = charge_data[self.charge_type] or {}
        confirmation_url = charge_data['confirmationUrl']
        errors = charge_data['userErrors']

        return ChargeCreateResponse(
            id=charge_info.get('id'), name=charge_info.get('name'), status=charge_info.get('status'),
            charge_type=charge_info.get('__typename'), confirmation_url=confirmation_url, errors=errors
        )

    def common_fields(self) -> str:
        return """
            confirmationUrl
            userErrors {
                field
                message
            }
        """

    def specific_fields(self) -> str:
        return """
            %s {
                id
                name
                status
                __typename
            }
        """ % self.charge_type

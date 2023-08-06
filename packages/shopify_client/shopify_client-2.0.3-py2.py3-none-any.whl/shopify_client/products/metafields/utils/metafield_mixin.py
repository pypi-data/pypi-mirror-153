import json


class MetafieldMixin:
    def parse_response(self, response):
        json_response = json.loads(response)
        try:
            metafields = json_response['data']['productUpdate']['product']['metafields']['edges']
        except KeyError:
            parsed_response = [{'message': error['message']} for error in json_response['errors']]
        else:
            parsed_response = [metafield['node'] for metafield in metafields]

        return parsed_response

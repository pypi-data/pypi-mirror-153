from shopify_client.common.mixins import UserErrorParserMixin
from .base import BaseScriptTag
from ..schema.request import ScriptTagDeleteRequest
from ..schema.response import ScriptTagDeleteResponse


class ScriptTagDelete(BaseScriptTag, UserErrorParserMixin):
    def delete(self, request: ScriptTagDeleteRequest):
        return self.execute(request)

    def generate_mutation(self) -> str:
        return '''
            mutation scriptTagDelete($id: ID!) {
                scriptTagDelete(id: $id) {
                    userErrors {
                        field
                        message
                    }
                    deletedScriptTagId
                }
            }
        '''

    def get_variables(self, request: ScriptTagDeleteRequest) -> dict:
        return {
            'id': request.id
        }

    def parse_response(self, response):
        response_object = response['data']['scriptTagDelete']

        return ScriptTagDeleteResponse(
            deleted_script_tag_id=response_object['deletedScriptTagId'],
            user_errors=self.parse_user_error(response_object['userErrors'])
        )

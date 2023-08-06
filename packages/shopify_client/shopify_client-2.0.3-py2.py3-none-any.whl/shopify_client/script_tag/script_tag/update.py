from shopify_client.common.mixins import UserErrorParserMixin
from .base import BaseScriptTag
from ..mixins import ScriptTagParserMixin
from ..schema.request import ScriptTagUpdateRequest
from ..schema.response import ScriptTagResponse


class ScriptTagUpdate(BaseScriptTag, UserErrorParserMixin, ScriptTagParserMixin):
    def update(self, request: ScriptTagUpdateRequest):
        return self.execute(request)

    def generate_mutation(self) -> str:
        return '''
            mutation scriptTagUpdate($id: ID!, $input: ScriptTagInput!) {
                scriptTagUpdate(id: $id, input: $input) {
                    userErrors {
                        field
                        message
                    }
                    scriptTag {
                        id
                        cache
                        displayScope
                        src
                        createdAt
                        updatedAt
                    }
                }
            }
        '''

    def get_variables(self, request: ScriptTagUpdateRequest) -> dict:
        return {
            'id': request.id,
            'input': {
                'cache': request.script_tag_input.cache,
                'displayScope': request.script_tag_input.display_scope,
                'src': request.script_tag_input.src
            }
        }

    def parse_response(self, response):
        response_object = response['data']['scriptTagUpdate']

        return ScriptTagResponse(
            script_tag=self.parse_script_tag(response_object['scriptTag']),
            user_errors=self.parse_user_error(response_object['userErrors'])
        )

from shopify_client.common.mixins import UserErrorParserMixin
from .base import BaseScriptTag
from ..mixins import ScriptTagParserMixin
from ..schema.request import ScriptTagInput
from ..schema.response import ScriptTagResponse


class ScriptTagCreate(BaseScriptTag, UserErrorParserMixin, ScriptTagParserMixin):
    def create(self, request: ScriptTagInput):
        return self.execute(request)

    def generate_mutation(self) -> str:
        return '''
            mutation scriptTagCreate($input: ScriptTagInput!) {
                scriptTagCreate(input: $input) {
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

    def get_variables(self, request: ScriptTagInput) -> dict:
        return {
            'input': {
                'cache': request.cache,
                'displayScope': request.display_scope,
                'src': request.src
            }
        }

    def parse_response(self, response):
        response_object = response['data']['scriptTagCreate']

        return ScriptTagResponse(
            script_tag=self.parse_script_tag(response_object['scriptTag']),
            user_errors=self.parse_user_error(response_object['userErrors'])
        )

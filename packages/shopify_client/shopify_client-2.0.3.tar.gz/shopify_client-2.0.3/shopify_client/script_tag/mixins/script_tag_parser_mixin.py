from typing import Optional

from ..schema.response import ScriptTag


class ScriptTagParserMixin:
    def parse_script_tag(self, response) -> Optional[ScriptTag]:
        if not response:
            return

        return ScriptTag(
            id=response['id'],
            src=response['src'],
            cache=response['cache'],
            display_scope=response['displayScope'],
            created_at=response['createdAt'],
            updated_at=response['updatedAt']
        )

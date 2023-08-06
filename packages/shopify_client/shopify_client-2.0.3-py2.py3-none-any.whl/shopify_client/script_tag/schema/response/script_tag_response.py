import dataclasses

from shopify_client.common.schema.response import UserError
from .script_tag import ScriptTag


@dataclasses.dataclass
class ScriptTagResponse:
    script_tag: ScriptTag
    user_errors: [UserError]

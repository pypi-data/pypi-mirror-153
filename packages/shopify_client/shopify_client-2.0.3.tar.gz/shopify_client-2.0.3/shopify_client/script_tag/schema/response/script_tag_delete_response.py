import dataclasses

from shopify_client.common.schema.response import UserError


@dataclasses.dataclass
class ScriptTagDeleteResponse:
    deleted_script_tag_id: str
    user_errors: [UserError]

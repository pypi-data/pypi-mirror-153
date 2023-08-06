import dataclasses

from shopify_client.script_tag.constants import ScriptTagDisplayScope


@dataclasses.dataclass
class ScriptTagInput:
    src: str
    cache: bool = False
    display_scope: str = ScriptTagDisplayScope.ALL.value

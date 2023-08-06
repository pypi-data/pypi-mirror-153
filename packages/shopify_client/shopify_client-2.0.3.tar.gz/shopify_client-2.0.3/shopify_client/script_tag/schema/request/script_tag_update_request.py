import dataclasses

from .script_tag_input import ScriptTagInput


@dataclasses.dataclass
class ScriptTagUpdateRequest:
    id: str
    script_tag_input: ScriptTagInput

import dataclasses


@dataclasses.dataclass
class ScriptTag:
    id: str
    src: str
    cache: bool
    display_scope: str
    created_at: str
    updated_at: str

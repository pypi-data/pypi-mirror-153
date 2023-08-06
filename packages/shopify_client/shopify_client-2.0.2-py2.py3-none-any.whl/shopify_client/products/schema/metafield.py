import dataclasses
from typing import Any


@dataclasses.dataclass
class Metafield:
    namespace: str
    key: str
    value: Any
    data_type: str

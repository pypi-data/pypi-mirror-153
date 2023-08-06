import dataclasses
from typing import Any


@dataclasses.dataclass
class MetafieldUpdate:
    id: str
    value: Any

import dataclasses
from typing import List

from .metafield_update import MetafieldUpdate


@dataclasses.dataclass
class ProductMetafieldUpdateInput:
    product_id: str
    namespace: str
    metafields: List[MetafieldUpdate]

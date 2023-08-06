import dataclasses
from typing import List

from .metafield import Metafield


@dataclasses.dataclass
class ProductMetafieldInput:
    product_id: str
    metafields: List[Metafield]

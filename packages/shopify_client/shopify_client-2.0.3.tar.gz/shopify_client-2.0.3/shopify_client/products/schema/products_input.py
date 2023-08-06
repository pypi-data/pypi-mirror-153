import dataclasses


@dataclasses.dataclass
class ProductsInput:
    first: int = None
    last: int = None
    reverse: bool = False
    after: str = None
    before: str = None
    query: str = None

    metafields_first: int = None
    metafields_namespace: str = None

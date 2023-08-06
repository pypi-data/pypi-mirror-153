import dataclasses


@dataclasses.dataclass
class Price:
    amount: str
    currencyCode: str = 'USD'

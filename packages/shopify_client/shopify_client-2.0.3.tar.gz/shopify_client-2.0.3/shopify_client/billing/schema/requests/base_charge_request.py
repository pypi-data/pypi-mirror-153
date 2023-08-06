import dataclasses


@dataclasses.dataclass
class BaseChargeRequest:
    name: str
    returnUrl: str

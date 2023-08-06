import dataclasses


@dataclasses.dataclass
class ChargeCreateResponse:
    id: str
    name: str
    status: str
    charge_type: str
    confirmation_url: str
    errors: [dict]

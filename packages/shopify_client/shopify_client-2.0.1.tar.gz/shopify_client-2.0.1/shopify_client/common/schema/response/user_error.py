import dataclasses


@dataclasses.dataclass
class UserError:
    field: [str]
    message: str

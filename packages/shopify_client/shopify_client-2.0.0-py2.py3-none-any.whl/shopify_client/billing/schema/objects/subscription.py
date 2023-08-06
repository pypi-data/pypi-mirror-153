import dataclasses


@dataclasses.dataclass
class AppSubscriptionObject:
    id: str
    name: str
    status: str

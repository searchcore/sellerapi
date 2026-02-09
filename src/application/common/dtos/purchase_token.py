from dataclasses import dataclass


@dataclass(frozen=True)
class PurchaseTokenDTO:
    id: int
    token: str

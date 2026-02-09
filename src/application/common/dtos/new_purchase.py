from dataclasses import dataclass


@dataclass(frozen=True)
class NewPurchaseDTO:
    token_id: int
    product_id: int

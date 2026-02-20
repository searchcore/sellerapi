from dataclasses import dataclass

from datetime import datetime

from src.domain.common.value_objects import ProductTypeIDVO


@dataclass(frozen=True)
class PurchaseTokenDataDTO:
    id: int
    product_type: ProductTypeIDVO
    token: str
    expires_at: datetime
    is_active: bool
    available_to_buy: int
    used_count: int

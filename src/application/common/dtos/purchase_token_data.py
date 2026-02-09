from dataclasses import dataclass

from datetime import datetime


@dataclass(frozen=True)
class PurchaseTokenDataDTO:
    id: int
    token: str
    expires_at: datetime
    is_active: bool
    available_to_buy: int
    used_count: int

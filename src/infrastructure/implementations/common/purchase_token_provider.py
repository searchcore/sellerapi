from typing import NewType

from src.application.common.interfaces import IPurchaseTokenProvider

from src.application.common.dtos import PurchaseTokenDTO


ScopedPurchaseToken = NewType("ScopedPurchaseToken", PurchaseTokenDTO | None)

class PurchaseTokenProvider(IPurchaseTokenProvider):
    def __init__(self, token: ScopedPurchaseToken):
        self._token = token

    def get_token(self) -> PurchaseTokenDTO:
        if self._token is None:
            raise ValueError("Context purchase token is absent")
        return self._token

from src.application.common.interfaces.purchase_token_provider import IPurchaseTokenProvider

from src.application.common.dtos import PurchaseTokenDTO


class FakePurchaseTokenProvider(IPurchaseTokenProvider):
    def __init__(self, purchase_token: PurchaseTokenDTO):
        self.purchase_token = purchase_token

    def get_token(self) -> PurchaseTokenDTO:
        return self.purchase_token

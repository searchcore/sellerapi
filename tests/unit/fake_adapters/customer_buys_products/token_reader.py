from src.application.customer_buys_products.interfaces import ITokenReader

from src.application.common.exceptions import PurchaseTokenNotFound
from src.application.common.dtos.purchase_token_data import PurchaseTokenDataDTO


class FakeTokenReader(ITokenReader):
    def __init__(self):
        self.tokens: list[PurchaseTokenDataDTO] = []

    async def get_token_data(self, token_id: int) -> PurchaseTokenDataDTO:
        for t in self.tokens:
            if t.id == token_id:
                return t
        
        raise PurchaseTokenNotFound("Token not found")

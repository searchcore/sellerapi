from src.application.customer_buys_products.interfaces import ITokenWriter

from src.application.common.dtos.purchase_token_data import PurchaseTokenDataDTO


class FakeTokenWriter(ITokenWriter):
    def __init__(self):
        self.tokens: list[PurchaseTokenDataDTO] = []

    async def add_to_used_count(self, token_id: int, used_count: int) -> None:
        for i, t in enumerate(self.tokens):
            if t.id == token_id:
                self.tokens[i] = PurchaseTokenDataDTO(t.id,t.token, t.expires_at, t.is_active, t.available_to_buy, t.used_count + used_count)
                return 
        raise ValueError()

    async def sub_available_to_buy(self, token_id: int, bought: int) -> None:
        for i, t in enumerate(self.tokens):
            if t.id == token_id:
                self.tokens[i] = PurchaseTokenDataDTO(t.id,t.token, t.expires_at, t.is_active, t.available_to_buy - bought, t.used_count)
                return
        raise ValueError()

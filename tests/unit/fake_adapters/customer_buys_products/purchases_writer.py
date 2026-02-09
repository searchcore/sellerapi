from src.application.customer_buys_products.interfaces import IPurchasesWriter

from src.application.common.dtos import NewPurchaseDTO


class FakePurchasesWriter(IPurchasesWriter):
    def __init__(self):
        self.purchases: list[NewPurchaseDTO] = []

    async def add_purchases(self, purchases: list[NewPurchaseDTO]) -> None:
        self.purchases.extend(purchases)

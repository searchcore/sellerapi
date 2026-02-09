from src.application.customer_buys_products.interfaces import IProductsReader

from src.application.common.dtos import ProductDTO


class FakeProductsReader(IProductsReader):
    def __init__(self):
        self.products: list[ProductDTO] = []

    async def get_unsold_unreserved_products(self, type: int, amount: int) -> list[ProductDTO]:
        p = [p for p in self.products if p.type == type]
        return p[:amount]

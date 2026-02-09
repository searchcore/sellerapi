from src.application.admin_manages_products.interfaces import IProductsWriter
from src.application.common.dtos import NewProductDTO


class FakeProductsWriter(IProductsWriter):
    def __init__(self):
        self.products: list[NewProductDTO] = []

    async def add_products(self, products: list[NewProductDTO]) -> None:
        self.products.extend(products)

from src.application.customer_buys_products.interfaces import IProductsWriter

from typing import Any

from src.application.common.dtos import ProductDTO


class FakeProductsWriter(IProductsWriter):
    def __init__(self):
        self.products: list[ProductDTO] = []

    async def set_content(self, products: list[ProductDTO], content: dict[str, Any]) -> None:
        self.products = [
            ProductDTO(
                p.id,
                p.type,
                content
            )
            for p
            in products
        ]

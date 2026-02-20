from abc import ABC, abstractmethod

from src.domain.common.value_objects import ProductTypeIDVO

from src.application.common.dtos import NewProductDTO


class IProductsWriter(ABC):
    @abstractmethod
    async def add_product_type(self, name: str) -> ProductTypeIDVO:
        ...

    @abstractmethod
    async def add_products(self, products: list[NewProductDTO]) -> None:
        ...

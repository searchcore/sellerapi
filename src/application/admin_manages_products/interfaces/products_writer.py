from abc import ABC, abstractmethod

from src.application.common.dtos import NewProductDTO


class IProductsWriter(ABC):
    @abstractmethod
    async def add_products(self, products: list[NewProductDTO]) -> None:
        ...

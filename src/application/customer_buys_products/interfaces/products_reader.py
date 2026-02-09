from abc import ABC, abstractmethod

from src.application.common.dtos import ProductDTO


class IProductsReader(ABC):
    @abstractmethod
    async def get_unsold_unreserved_products(self, type: int, amount: int) -> list[ProductDTO]:
        ...

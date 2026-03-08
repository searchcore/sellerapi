from abc import ABC, abstractmethod

from src.domain.common.value_objects import ProductTypeIDVO
from src.application.common.dtos import ProductDTO


class IProductsReader(ABC):
    @abstractmethod
    async def get_unsold_unreserved_products(self, type: int, amount: int, with_features: list[int]) -> list[ProductDTO]:
        ...

    @abstractmethod
    async def get_unsold_unreserved_products_count(self, type: ProductTypeIDVO, with_features: list[int]) -> int:
        ...

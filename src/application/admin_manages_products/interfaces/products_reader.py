from abc import ABC, abstractmethod
from typing import Any

from src.application.admin_manages_products.dtos import ProductTypeWithSchemaDTO
from src.application.common.dtos import ProductDTO
from src.domain.common.value_objects import ProductTypeIDVO


class IProductsReader(ABC):
    @abstractmethod
    async def does_product_type_exist(self, id: ProductTypeIDVO) -> bool:
        ...

    @abstractmethod
    async def get_products_types(self, offset: int, limit: int) -> list[ProductTypeWithSchemaDTO]:
        ...

    @abstractmethod
    async def get_products_types_total(self) -> int:
        ...

    @abstractmethod
    async def find_products(
        self,
        product_type: ProductTypeIDVO,
        contains: dict[str, Any] | None = None,
    ) -> list[ProductDTO]:
        ...

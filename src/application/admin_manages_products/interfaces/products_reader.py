from abc import ABC, abstractmethod

from src.domain.common.value_objects import ProductTypeIDVO
from src.application.admin_manages_products.dtos import ProductTypeWithSchemaDTO


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

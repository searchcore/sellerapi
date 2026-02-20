from abc import ABC, abstractmethod

from src.domain.common.value_objects import ProductTypeIDVO, ProductTypeSchemaVersionVO

from src.application.admin_manages_products.dtos import ProductTypeSchemaDTO


class ISchemaReader(ABC):
    @abstractmethod
    async def get_schema_for_product_type_and_version(self, product_type: ProductTypeIDVO, schema_version: ProductTypeSchemaVersionVO) -> ProductTypeSchemaDTO | None:
        ...

    @abstractmethod
    async def get_schema_with_biggest_version(self, product_type: ProductTypeIDVO) -> ProductTypeSchemaDTO:
        ...

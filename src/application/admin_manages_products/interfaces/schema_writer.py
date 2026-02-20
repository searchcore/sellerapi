from abc import ABC, abstractmethod

from src.domain.common.value_objects import ProductTypeIDVO, ProductTypeSchemaVO, ProductTypeSchemaIDVO, ProductTypeSchemaVersionVO


class ISchemaWriter(ABC):
    @abstractmethod
    async def add_product_type_schema(
        self,
        product_type: ProductTypeIDVO,
        version: ProductTypeSchemaVersionVO,
        schema: ProductTypeSchemaVO
    ) -> ProductTypeSchemaIDVO:
        ...

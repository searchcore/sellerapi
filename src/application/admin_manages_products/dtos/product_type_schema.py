from dataclasses import dataclass

from src.domain.common.value_objects import ProductTypeSchemaIDVO, ProductTypeSchemaVersionVO, ProductTypeSchemaVO


@dataclass(frozen=True)
class ProductTypeSchemaDTO:
    id: ProductTypeSchemaIDVO
    version: ProductTypeSchemaVersionVO
    schema: ProductTypeSchemaVO

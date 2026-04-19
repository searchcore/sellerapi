from dataclasses import dataclass

from src.domain.common.value_objects import ProductTypeIDVO

from .product_type_schema import ProductTypeSchemaDTO


@dataclass(frozen=True)
class ProductTypeWithSchemaDTO:
    id: ProductTypeIDVO
    name: str
    current_schema: ProductTypeSchemaDTO

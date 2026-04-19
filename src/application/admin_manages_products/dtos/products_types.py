from dataclasses import dataclass

from .product_type_with_schema import ProductTypeWithSchemaDTO


@dataclass(frozen=True)
class ProductsTypesDTO:
    products_types: list[ProductTypeWithSchemaDTO]
    total: int

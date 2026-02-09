from dataclasses import dataclass

from src.application.common.content_validators import ProductValidationReport


@dataclass(frozen=True)
class AddProductsResultDTO:
    added_products_amount: int
    not_added_products: list[ProductValidationReport]

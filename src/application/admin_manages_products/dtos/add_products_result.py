from dataclasses import dataclass

from src.application.common.interfaces.schema_validator import ContentValidationReport


@dataclass(frozen=True)
class ImportProductsResultDTO:
    added_products_amount: int
    not_added_products: list[ContentValidationReport]

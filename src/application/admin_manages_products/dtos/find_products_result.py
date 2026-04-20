from dataclasses import dataclass

from src.application.common.dtos import ProductDTO


@dataclass(frozen=True)
class FindProductsResultDTO:
    result: list[ProductDTO]


from abc import ABC, abstractmethod

from typing import Any

from src.application.common.dtos import ProductDTO


class IProductsWriter(ABC):
    @abstractmethod
    async def set_content(self, products: list[ProductDTO], content: dict[str, Any]) -> None:
        ...

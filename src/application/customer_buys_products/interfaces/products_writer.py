from abc import ABC, abstractmethod

from datetime import datetime

from src.application.common.dtos import ProductDTO


class IProductsWriter(ABC):
    @abstractmethod
    async def set_reserved(self, products: list[ProductDTO], until: datetime):
        ...

    @abstractmethod
    async def set_valid(self, products: list[ProductDTO], valid: bool):
        ...

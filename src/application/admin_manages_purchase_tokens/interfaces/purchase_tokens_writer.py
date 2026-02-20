from abc import ABC, abstractmethod

from datetime import datetime

from src.domain.common.value_objects import ProductTypeIDVO


class IPurchaseTokensWriter(ABC):
    @abstractmethod
    async def add_token(self, product_type: ProductTypeIDVO, token: str, expires_at: datetime, available_to_buy: int) -> int:
        ...

    @abstractmethod
    async def add_to_available_to_buy(self, token_id: int, to_add: int) -> None:
        ...

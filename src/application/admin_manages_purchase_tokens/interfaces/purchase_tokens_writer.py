from abc import ABC, abstractmethod

from datetime import datetime


class IPurchaseTokensWriter(ABC):
    @abstractmethod
    async def add_token(self, token: str, expires_at: datetime, available_to_buy: int) -> int:
        ...

    @abstractmethod
    async def add_to_available_to_buy(self, token_id: int, to_add: int) -> None:
        ...

from abc import ABC, abstractmethod

from src.application.common.dtos import NewPurchaseDTO


class IPurchasesWriter(ABC):
    @abstractmethod
    async def add_purchases(self, purchases: list[NewPurchaseDTO]) -> None:
        ...

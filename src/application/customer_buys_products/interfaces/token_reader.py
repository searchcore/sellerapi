from abc import ABC, abstractmethod

from src.application.common.dtos import PurchaseTokenDataDTO


class ITokenReader(ABC):
    @abstractmethod
    async def get_token_data(self, token_id: int) -> PurchaseTokenDataDTO:
        ...

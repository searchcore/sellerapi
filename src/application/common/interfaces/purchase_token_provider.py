from abc import ABC, abstractmethod

from src.application.common.dtos import PurchaseTokenDTO


class IPurchaseTokenProvider(ABC):
    @abstractmethod
    def get_token(self) -> PurchaseTokenDTO:
        ...

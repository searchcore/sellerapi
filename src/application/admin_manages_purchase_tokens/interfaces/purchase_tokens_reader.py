from abc import ABC, abstractmethod


class IPurchaseTokensReader(ABC):
    @abstractmethod
    async def is_token_exist(self, token_id: int) -> bool:
        ...

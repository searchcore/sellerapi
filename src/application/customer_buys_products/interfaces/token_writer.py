from abc import ABC, abstractmethod


class ITokenWriter(ABC):
    @abstractmethod
    async def add_to_used_count(self, token_id: int, used_count: int) -> None:
        ...

    @abstractmethod
    async def sub_available_to_buy(self, token_id: int, bought: int) -> None:
        ...

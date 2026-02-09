from abc import ABC, abstractmethod

from contextlib import AbstractAsyncContextManager


class IUoW(ABC):
    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...

    @abstractmethod
    async def flush(self):
        ...

    @abstractmethod
    async def transaction(self) -> AbstractAsyncContextManager["IUoW"]:
        ...

from src.application.common.interfaces import IUoW

from contextlib import asynccontextmanager
from typing import AsyncIterator


class FakeUoW(IUoW):
    def __init__(self):
        self.commited = False
        self.rolled_back = False

    async def commit(self):
        self.commited = True

    async def rollback(self):
        self.rolled_back = True

    async def flush(self):
        ...

    @asynccontextmanager
    async def transaction(self) -> AsyncIterator["IUoW"]:
        yield self

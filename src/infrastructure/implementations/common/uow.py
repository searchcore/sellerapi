from sqlalchemy.ext.asyncio import AsyncSession

from contextlib import asynccontextmanager
from typing import AsyncIterator

from src.application.common.interfaces import IUoW


class UoW(IUoW):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()

    async def flush(self):
        await self._session.flush()

    @asynccontextmanager
    async def transaction(self) -> AsyncIterator["UoW"]:
        async with self._session.begin_nested():
            yield self

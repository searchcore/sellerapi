import pytest

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from src.db.factory import build_sa_engine, build_sa_session_factory

from src.core.config import DatabaseConfig


DSN = "postgresql+asyncpg://postgres:postgres@localhost:5432/database"


@pytest.fixture
def database_cfg() -> DatabaseConfig:
    return DatabaseConfig(DSN)


@pytest.fixture
async def engine(database_cfg: DatabaseConfig):
    g = build_sa_engine(database_cfg)
    yield await anext(g)
    try:
        await anext(g)
    except StopAsyncIteration:
        ...


@pytest.fixture
async def session_factory(engine: AsyncEngine):
    yield build_sa_session_factory(engine)


@pytest.fixture
async def session(session_factory: async_sessionmaker[AsyncSession]):
    async with session_factory() as session:
        tx = await session.begin()
        try:
            yield session
        finally:
            await tx.rollback()

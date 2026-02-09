import pytest

from sqlalchemy import text

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
    factory = build_sa_session_factory(engine)

    try:
        yield factory
    finally:
        async with engine.begin() as conn:
            await conn.execute(text("TRUNCATE access_tokens, products, product_purchases, product_types, purchase_tokens RESTART IDENTITY CASCADE"))


@pytest.fixture
async def session(session_factory: async_sessionmaker[AsyncSession]):
    async with session_factory() as session:
        async with session.begin():
            yield session
            await session.rollback()

from dishka import Provider, Scope

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, AsyncSession

from src.db.factory import build_sa_engine, build_sa_session, build_sa_session_factory


def setup_provider(provider: Provider):
    provider.provide(source=build_sa_engine, scope=Scope.APP, provides=AsyncEngine)
    provider.provide(source=build_sa_session_factory, scope=Scope.APP, provides=async_sessionmaker[AsyncSession])
    provider.provide(source=build_sa_session, scope=Scope.REQUEST, provides=AsyncSession)

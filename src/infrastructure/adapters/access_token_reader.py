from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.dtos import AccessTokenBriefDTO

from src.db.models import AccessTokenModel


class AccessTokenReader:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get(self, token_hash: str) -> AccessTokenBriefDTO | None:
        stmt = select(AccessTokenModel).where(
            AccessTokenModel.token_hash == token_hash
        )
        r = await self._session.execute(stmt)
        m = r.scalar()

        if m is None:
            return None

        return AccessTokenBriefDTO(m.id, m.token_hash)

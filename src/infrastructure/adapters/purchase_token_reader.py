from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.dtos import PurchaseTokenDTO

from src.db.models import PurchaseTokenModel


class PurchaseTokenReader:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get(self, token: str) -> PurchaseTokenDTO | None:
        stmt = select(PurchaseTokenModel).where(
            PurchaseTokenModel.token == token
        )
        r = await self._session.execute(stmt)
        m = r.scalar()

        if m is None:
            return None

        return PurchaseTokenDTO(m.id, m.token)

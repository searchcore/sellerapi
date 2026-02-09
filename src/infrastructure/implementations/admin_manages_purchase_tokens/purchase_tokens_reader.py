from src.application.admin_manages_purchase_tokens.interfaces import IPurchaseTokensReader

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import PurchaseTokenModel


class PurchaseTokensReader(IPurchaseTokensReader):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def is_token_exist(self, token_id: int) -> bool:
        r = await self._session.execute(select(PurchaseTokenModel.id).where(PurchaseTokenModel.id == token_id))

        return bool(r.scalar_one_or_none())

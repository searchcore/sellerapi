from src.application.admin_manages_purchase_tokens.interfaces import IPurchaseTokensWriter

from src.domain.common.value_objects import ProductTypeIDVO

from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import PurchaseTokenModel


class PurchaseTokensWriter(IPurchaseTokensWriter):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add_token(self, product_type: ProductTypeIDVO, token: str, expires_at: datetime, available_to_buy: int) -> int:
        m = PurchaseTokenModel(
            product_type=product_type.value,
            token=token,
            expires_at=expires_at,
            available_to_buy=available_to_buy,
        )
        self._session.add(m)
        await self._session.flush()
        return m.id

    async def add_to_available_to_buy(self, token_id: int, to_add: int) -> None:
        m = await self._session.get_one(PurchaseTokenModel, token_id)

        m.available_to_buy += to_add

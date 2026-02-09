from src.application.customer_buys_products.interfaces import ITokenWriter

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import PurchaseTokenModel


class TokenWriter(ITokenWriter):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add_to_used_count(self, token_id: int, used_count: int) -> None:
        m = await self._session.get_one(PurchaseTokenModel, token_id)
        m.used_count += used_count

    async def sub_available_to_buy(self, token_id: int, bought: int) -> None:
        m = await self._session.get_one(PurchaseTokenModel, token_id)
        m.available_to_buy -= bought

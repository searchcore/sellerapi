from src.application.customer_buys_products.interfaces import IPurchasesWriter

from datetime import datetime, timezone

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.dtos import NewPurchaseDTO

from src.db.models import ProductPurchaseModel


class PurchasesWriter(IPurchasesWriter):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add_purchases(self, purchases: list[NewPurchaseDTO]) -> None:
        now = datetime.now(timezone.utc)
        await self._session.execute(
            insert(ProductPurchaseModel),
            [
                {"product_id": p.product_id, "token_id": p.token_id, "bought_at": now}
                for p
                in purchases
            ]
        )

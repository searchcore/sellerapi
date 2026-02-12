from src.application.customer_buys_products.interfaces import IProductsWriter

from typing import Any

from operator import attrgetter

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import ProductModel

from src.application.common.dtos import ProductDTO


class ProductsWriter(IProductsWriter):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def set_content(self, products: list[ProductDTO], content: dict[str, Any]):
        stmt = (
            update(ProductModel)
            .values(content=content)
            .where(
                ProductModel.id.in_(map(attrgetter('id'), products))
            )
        )
        await self._session.execute(stmt)

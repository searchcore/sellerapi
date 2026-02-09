from src.application.admin_manages_products.interfaces import IProductsWriter
from src.application.common.dtos import NewProductDTO

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import ProductModel


class ProductsWriter(IProductsWriter):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add_products(self, products: list[NewProductDTO]) -> None:
        await self._session.execute(
            insert(ProductModel),
            [
                {"type": p.product_type_id, "content": p.content}
                for p
                in products
            ]
        )

from src.application.customer_buys_products.interfaces import IProductsReader

from sqlalchemy import select, exists, or_, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import ProductModel, ProductPurchaseModel

from src.domain.common.value_objects import ProductTypeIDVO
from src.application.common.dtos import ProductDTO


class ProductsReader(IProductsReader):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_unsold_unreserved_products(self, type: int, amount: int) -> list[ProductDTO]:
        stmt = (
            select(ProductModel.id, ProductModel.content)
            .where(
                ProductModel.type == type,
                ProductModel.valid == True,
                or_(ProductModel.reserved_until.is_(None), ProductModel.reserved_until < func.now()),
                ~exists().where(ProductPurchaseModel.product_id == ProductModel.id)
            )
            .order_by(ProductModel.created_at.desc())
            .with_for_update(skip_locked=True)
            .limit(amount)          
        )

        result = await self._session.execute(stmt)

        return [ProductDTO(row.id, type, row.content) for row in result.all()]

    async def get_unsold_unreserved_products_count(self, type: ProductTypeIDVO) -> int:
        stmt = (
            select(func.count(ProductModel.id))
            .where(
                ProductModel.type == type.value,
                ProductModel.valid == True,
                or_(ProductModel.reserved_until.is_(None), ProductModel.reserved_until < func.now()),
                ~exists().where(ProductPurchaseModel.product_id == ProductModel.id)
            )      
        )

        result = await self._session.scalar(stmt)

        return result or 0

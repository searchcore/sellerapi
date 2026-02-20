from src.application.admin_manages_products.interfaces import IProductsReader

from src.domain.common.value_objects import ProductTypeIDVO

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import ProductTypeModel


class ProductsReader(IProductsReader):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def does_product_type_exist(self, id: ProductTypeIDVO) -> bool:
        return bool(await self._session.get(ProductTypeModel, id.value))

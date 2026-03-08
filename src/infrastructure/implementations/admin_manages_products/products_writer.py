from src.application.admin_manages_products.interfaces import IProductsWriter
from src.application.common.dtos import NewProductDTO
from src.domain.common.value_objects import ProductTypeIDVO, ProductTypeSchemaIDVO

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import ProductModel, ProductTypeModel, ProductFeaturesModel


class ProductsWriter(IProductsWriter):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add_product_type(self, name: str) -> ProductTypeIDVO:
        m = ProductTypeModel(name=name)
        self._session.add(m)
        await self._session.flush()
        return ProductTypeIDVO(m.id)

    async def add_products(self, schema: ProductTypeSchemaIDVO, products: list[NewProductDTO], features: list[int]) -> None:
        result = await self._session.execute(
            insert(ProductModel)
            .returning(ProductModel.id),
            [
                {"type": p.product_type_id, "schema": schema.value, "content": p.content}
                for p
                in products
            ]
        )

        products_ids = result.scalars().all()

        entries = []
        for product_id in products_ids:
            for feature_id in features:
                entries.append({"product_id": product_id, "feature_id": feature_id})

        if entries:
            await self._session.execute(
                insert(ProductFeaturesModel),
                entries,
            )

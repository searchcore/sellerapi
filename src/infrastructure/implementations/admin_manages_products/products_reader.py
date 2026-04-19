from src.application.admin_manages_products.interfaces import IProductsReader
from src.application.admin_manages_products.dtos import ProductTypeWithSchemaDTO, ProductTypeSchemaDTO

from src.domain.common.value_objects import ProductTypeIDVO, ProductTypeSchemaIDVO, ProductTypeSchemaVersionVO, ProductTypeSchemaVO

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from src.db.models import ProductTypeModel, ProductSchemaVersionModel


class ProductsReader(IProductsReader):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def does_product_type_exist(self, id: ProductTypeIDVO) -> bool:
        return bool(await self._session.get(ProductTypeModel, id.value))

    async def get_products_types(self, offset: int, limit: int) -> list[ProductTypeWithSchemaDTO]:
        latest_schema_version_sq = (
            select(
                ProductSchemaVersionModel.product_type,
                func.max(ProductSchemaVersionModel.version).label("latest_version"),
            )
            .group_by(ProductSchemaVersionModel.product_type)
            .subquery()
        )

        stmt = (
            select(
                ProductTypeModel.id,
                ProductTypeModel.name,
                ProductSchemaVersionModel.id.label("schema_id"),
                ProductSchemaVersionModel.version,
                ProductSchemaVersionModel.schema,
            )
            .join(
                latest_schema_version_sq,
                latest_schema_version_sq.c.product_type == ProductTypeModel.id,
            )
            .join(
                ProductSchemaVersionModel,
                (
                    ProductSchemaVersionModel.product_type == latest_schema_version_sq.c.product_type
                ) & (
                    ProductSchemaVersionModel.version == latest_schema_version_sq.c.latest_version
                )
            )
            .order_by(ProductTypeModel.id.asc())
            .offset(offset)
            .limit(limit)
        )

        result = await self._session.execute(stmt)

        return [
            ProductTypeWithSchemaDTO(
                id=ProductTypeIDVO(row.id),
                name=row.name,
                current_schema=ProductTypeSchemaDTO(
                    id=ProductTypeSchemaIDVO(row.schema_id),
                    version=ProductTypeSchemaVersionVO(row.version),
                    schema=ProductTypeSchemaVO(row.schema),
                ),
            )
            for row in result.all()
        ]

    async def get_products_types_total(self) -> int:
        stmt = select(func.count(ProductTypeModel.id)).where(
            select(ProductSchemaVersionModel.id)
            .where(ProductSchemaVersionModel.product_type == ProductTypeModel.id)
            .exists()
        )

        result = await self._session.scalar(stmt)
        return result or 0

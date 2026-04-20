from typing import Any

from src.application.admin_manages_products.interfaces import IProductsReader
from src.application.admin_manages_products.dtos import ProductTypeWithSchemaDTO, ProductTypeSchemaDTO
from src.application.common.dtos import ProductDTO

from src.domain.common.value_objects import ProductTypeIDVO, ProductTypeSchemaIDVO, ProductTypeSchemaVersionVO, ProductTypeSchemaVO

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, cast
from sqlalchemy.dialects.postgresql import JSONB

from src.db.models import ProductTypeModel, ProductSchemaVersionModel, ProductModel


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

    async def find_products(
        self,
        product_type: ProductTypeIDVO,
        contains: dict[str, Any] | None = None,
    ) -> list[ProductDTO]:
        stmt = (
            select(
                ProductModel.id,
                ProductModel.type,
                ProductModel.content,
            )
            .where(*self._build_find_products_filters(product_type, contains))
            .order_by(ProductModel.id.asc())
        )

        result = await self._session.execute(stmt)

        return [
            ProductDTO(
                id=row.id,
                type=row.type,
                content=row.content,
            )
            for row in result.all()
        ]

    def _build_find_products_filters(
        self,
        product_type: ProductTypeIDVO,
        contains: dict[str, Any] | None,
    ) -> list[Any]:
        filters: list[Any] = [ProductModel.type == product_type.value]

        if contains is not None:
            filters.append(ProductModel.content.op("@>")(cast(contains, JSONB)))

        return filters

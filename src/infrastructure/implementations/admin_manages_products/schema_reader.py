from src.application.admin_manages_products.interfaces import ISchemaReader

from src.domain.common.value_objects import ProductTypeIDVO, ProductTypeSchemaVO, ProductTypeSchemaIDVO, ProductTypeSchemaVersionVO
from src.application.admin_manages_products.dtos import ProductTypeSchemaDTO
from src.application.common.exceptions import ProductTypeSchemaNotFound

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import ProductSchemaVersionModel


class SchemaReader(ISchemaReader):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_schema_for_product_type_and_version(self, product_type: ProductTypeIDVO, schema_version: ProductTypeSchemaVersionVO) -> ProductTypeSchemaDTO | None:
        stmt = (
            select(ProductSchemaVersionModel)
            .where(
                ProductSchemaVersionModel.product_type == product_type.value,
                ProductSchemaVersionModel.version == schema_version.value,
            )
        )

        model = await self._session.scalar(stmt)

        if model is None:
            return None
        
        return ProductTypeSchemaDTO(
            ProductTypeSchemaIDVO(model.id),
            ProductTypeSchemaVersionVO(model.version),
            ProductTypeSchemaVO(model.schema)
        )

    async def get_schema_with_biggest_version(self, product_type: ProductTypeIDVO) -> ProductTypeSchemaDTO:
        stmt = (
            select(ProductSchemaVersionModel)
            .where(
                ProductSchemaVersionModel.product_type == product_type.value,
            )
            .order_by(
                ProductSchemaVersionModel.version.desc()
            )
            .limit(1)
        )

        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()

        if model is None:
            raise ProductTypeSchemaNotFound("Schema not found when one must be present.")
        
        return ProductTypeSchemaDTO(
            ProductTypeSchemaIDVO(model.id),
            ProductTypeSchemaVersionVO(model.version),
            ProductTypeSchemaVO(model.schema)
        )

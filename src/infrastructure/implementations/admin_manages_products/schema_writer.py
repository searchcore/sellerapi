from src.application.admin_manages_products.interfaces import ISchemaWriter

from src.domain.common.value_objects import ProductTypeIDVO, ProductTypeSchemaVO, ProductTypeSchemaIDVO, ProductTypeSchemaVersionVO

from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import ProductSchemaVersionModel


class SchemaWriter(ISchemaWriter):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add_product_type_schema(
        self,
        product_type: ProductTypeIDVO,
        version: ProductTypeSchemaVersionVO,
        schema: ProductTypeSchemaVO
    ) -> ProductTypeSchemaIDVO:
        m = ProductSchemaVersionModel(
            product_type=product_type.value,
            version=version.value,
            schema=schema.value,
        )
        self._session.add(m)
        await self._session.flush()
        return ProductTypeSchemaIDVO(m.id)

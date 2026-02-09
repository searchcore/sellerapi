from src.infrastructure.implementations.customer_buys_products import ProductsReader

from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import insert
from src.db.models import ProductModel, ProductTypeModel


async def test_products_reader_skip_locked(session: AsyncSession):
    type_id = await session.scalar(
        insert(ProductTypeModel)
        .values(
            name="test"
        )
        .returning(ProductTypeModel.id)
    )

    assert type_id is not None # scalar int | None

    await session.execute(
        insert(ProductModel),
        [
            {"type": type_id, "content": {}}
            for _
            in range(10)
        ]
    )

    reader = ProductsReader(session)

    products = await reader.get_unsold_unreserved_products(type_id, 5)

    assert len(products) == 5

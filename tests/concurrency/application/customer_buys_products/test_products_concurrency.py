from src.infrastructure.implementations.customer_buys_products import ProductsReader

from operator import attrgetter

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from sqlalchemy import insert
from src.db.models import ProductModel, ProductTypeModel


async def test_products_reader_skip_locked(session_factory: async_sessionmaker[AsyncSession]):
    async with session_factory() as session:
        type_id = await session.scalar(
            insert(ProductTypeModel)
            .values(
                name="test"
            )
            .returning(ProductTypeModel.id)
        )

        assert type_id is not None

        await session.execute(
            insert(ProductModel),
            [
                {"type": type_id, "content": {}}
                for _
                in range(10)
            ]
        )
        await session.commit()

    async with session_factory() as session:
        reader = ProductsReader(session)

        products_1 = await reader.get_unsold_unreserved_products(type_id, 5)
        product_ids_1 = set(map(attrgetter("id"), products_1))

        assert len(product_ids_1) == 5

        async with session_factory() as concurent_session:
            concurent_reader = ProductsReader(concurent_session)

            products_2 = await concurent_reader.get_unsold_unreserved_products(type_id, 5)
            product_ids_2 = set(map(attrgetter("id"), products_2))

            assert len(product_ids_2) == 5

            assert product_ids_1 != product_ids_2

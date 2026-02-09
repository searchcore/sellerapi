from src.application.admin_manages_products.commands.add_products_without_validation import (
    AddProductsWithoutValidationCMD, 
    AddProductsWithouValidationCMDHandler
)
from tests.unit.fake_adapters.common.uow import FakeUoW
from tests.unit.fake_adapters.admin_manages_products.products_writer import FakeProductsWriter

from src.application.common.dtos import NewProductDTO


async def test_add_one_product_handler_success(
    uow: FakeUoW,
    products_writer: FakeProductsWriter,
):
    handler = AddProductsWithouValidationCMDHandler(
        uow,
        products_writer,
    )
    products = [NewProductDTO(13, {}), NewProductDTO(1, {"random": "content"})]
    cmd = AddProductsWithoutValidationCMD(products)

    result = await handler(cmd)

    assert result is None

    assert len(products_writer.products) == 2
    assert products_writer.products[0].product_type_id == 13
    assert products_writer.products[0].content == {}
    assert products_writer.products[1].product_type_id == 1
    assert products_writer.products[1].content == {"random": "content"}

    assert uow.commited == True
    assert uow.rolled_back == False

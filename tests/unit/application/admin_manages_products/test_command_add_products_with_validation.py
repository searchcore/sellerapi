from src.application.admin_manages_products.commands.add_products_with_validation import (
    AddProductsWithValidationCMDHandler,
    AddProductsWithValidationCMD,
)
from src.application.common.content_validators import ProductInvalidReason

from tests.unit.fake_adapters.common.uow import FakeUoW
from tests.unit.fake_adapters.common.validators_provider import FakeValidatorProvider
from tests.unit.fake_adapters.admin_manages_products.products_writer import FakeProductsWriter

from src.application.common.dtos import NewProductDTO


async def test_add_one_product_handler_success(
    uow: FakeUoW,
    products_writer: FakeProductsWriter,
    validator_provider: FakeValidatorProvider
):
    handler = AddProductsWithValidationCMDHandler(
        uow,
        products_writer,
        validator_provider,
    )
    product_type = 13
    product_content = {"some_content": "some_value"}
    products = [NewProductDTO(product_type, product_content)]
    cmd = AddProductsWithValidationCMD(product_type, products)

    result = await handler(cmd)

    assert result.added_products_amount == 1
    assert len(result.not_added_products) == 0

    assert len(products_writer.products) == 1
    assert products_writer.products[0].product_type_id == product_type
    assert products_writer.products[0].content == product_content

    assert uow.commited == True
    assert uow.rolled_back == False


async def test_add_empty_products_error(
    uow: FakeUoW,
    products_writer: FakeProductsWriter,
    validator_provider: FakeValidatorProvider
):
    handler = AddProductsWithValidationCMDHandler(
        uow,
        products_writer,
        validator_provider,
    )
    product_type = 13
    empty_products = [NewProductDTO(product_type, {}), NewProductDTO(product_type, {"field": ""})]
    cmd = AddProductsWithValidationCMD(product_type, empty_products)

    result = await handler(cmd)

    assert result.added_products_amount == 0
    assert len(products_writer.products) == 0
    assert len(result.not_added_products) == 2
    empty_product_validation_report = result.not_added_products[0]
    assert empty_product_validation_report.execution_error is None
    assert empty_product_validation_report.product_id == 0
    assert len(empty_product_validation_report.violations) == 1
    assert empty_product_validation_report.violations[0].details == "Empty product provided"

    no_value_product_report = result.not_added_products[1]
    assert no_value_product_report.execution_error is None
    assert no_value_product_report.product_id == 1
    assert len(no_value_product_report.violations) == 1
    assert no_value_product_report.violations[0].details == "Provided product does not contain any value"

    assert uow.commited == False
    assert uow.rolled_back == False


async def test_add_multiple_products_handler_success(
    uow: FakeUoW,
    products_writer: FakeProductsWriter,
    validator_provider: FakeValidatorProvider
):
    handler = AddProductsWithValidationCMDHandler(
        uow,
        products_writer,
        validator_provider,
    )
    product_type = 13
    content = {"some_content": "some_value"}
    empty_content = {}
    products = [
        NewProductDTO(product_type, content if i % 2 == 0 else empty_content) # even products valid
        for i
        in range(10)
    ]

    cmd = AddProductsWithValidationCMD(product_type, products)

    result = await handler(cmd)

    assert result.added_products_amount == 5
    assert len(result.not_added_products) == 5

    assert len(products_writer.products) == 5
    assert [p.content for p in products_writer.products] == [content] * 5

    assert len(result.not_added_products) == 5
    assert [report.product_id for report in result.not_added_products] == [1, 3, 5, 7, 9]
    assert [report.violations for report in result.not_added_products] == [[ProductInvalidReason("Empty product provided")]] * 5

    assert uow.commited == True
    assert uow.rolled_back == False

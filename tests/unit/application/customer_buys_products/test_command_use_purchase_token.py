from datetime import datetime
import pytest

from src.application.customer_buys_products.commands.use_purchase_token import (
    UsePurchaseTokenCMD,
    UsePurchaseTokenCMDHandler,
)
from tests.unit.fake_adapters.common.uow import FakeUoW
from tests.unit.fake_adapters.customer_buys_products.products_reader import FakeProductsReader
from tests.unit.fake_adapters.customer_buys_products.purchases_writer import FakePurchasesWriter
from tests.unit.fake_adapters.customer_buys_products.token_reader import FakeTokenReader
from tests.unit.fake_adapters.customer_buys_products.token_writer import FakeTokenWriter
from tests.unit.fake_adapters.customer_buys_products.purchase_token_provider import FakePurchaseTokenProvider

from src.application.common.dtos import PurchaseTokenDTO
from src.application.common.dtos import ProductDTO
from src.application.common.dtos.purchase_token_data import PurchaseTokenDataDTO

from src.application.common.exceptions import ProductOutOfStock
from src.application.customer_buys_products.exceptions import TokenLimitExceeded


async def test_use_purchase_token_once_success(
    uow: FakeUoW,
    products_reader: FakeProductsReader,
    purchase_token_provider: FakePurchaseTokenProvider,
    purchases_writer: FakePurchasesWriter,
    token_writer: FakeTokenWriter,
    token_reader: FakeTokenReader,
):
    TOKEN = PurchaseTokenDTO(1337, "abc")
    TOKEN_DATA = PurchaseTokenDataDTO(1337, "abc", datetime.now(), True, 100, 0)
    purchase_token_provider.purchase_token = TOKEN
    products_reader.products = [ProductDTO(1, 111, {"content": "content"})]
    token_reader.tokens = [TOKEN_DATA]
    token_writer.tokens = [TOKEN_DATA]

    handler = UsePurchaseTokenCMDHandler(
        uow,
        products_reader,
        purchase_token_provider,
        purchases_writer,
        token_writer,
        token_reader,
    )
    cmd = UsePurchaseTokenCMD(111, 1)

    products = await handler(cmd)

    assert len(products) == 1
    assert token_writer.tokens[0].used_count == TOKEN_DATA.used_count + 1
    assert token_writer.tokens[0].available_to_buy == TOKEN_DATA.available_to_buy - 1
    assert len(purchases_writer.purchases) == 1
    assert purchases_writer.purchases[0].product_id == 1
    assert purchases_writer.purchases[0].token_id == 1337

    assert uow.commited == True
    assert uow.rolled_back == False


async def test_use_purchase_token_once_out_of_stock(
    uow: FakeUoW,
    products_reader: FakeProductsReader,
    purchase_token_provider: FakePurchaseTokenProvider,
    purchases_writer: FakePurchasesWriter,
    token_writer: FakeTokenWriter,
    token_reader: FakeTokenReader,
):
    TOKEN = PurchaseTokenDTO(1337, "abc")
    TOKEN_DATA = PurchaseTokenDataDTO(1337, "abc", datetime.now(), True, 100, 0)
    purchase_token_provider.purchase_token = TOKEN
    products_reader.products = [ProductDTO(1, 111, {"content": "content"})]
    token_reader.tokens = [TOKEN_DATA]
    token_writer.tokens = [TOKEN_DATA]

    handler = UsePurchaseTokenCMDHandler(
        uow,
        products_reader,
        purchase_token_provider,
        purchases_writer,
        token_writer,
        token_reader,
    )
    cmd = UsePurchaseTokenCMD(111, 2)

    with pytest.raises(ProductOutOfStock) as exc_info:
        await handler(cmd)

    assert exc_info.value.params.get("available") == 1

    assert uow.commited == False
    assert uow.rolled_back == False


async def test_use_purchase_token_token_limit(
    uow: FakeUoW,
    products_reader: FakeProductsReader,
    purchase_token_provider: FakePurchaseTokenProvider,
    purchases_writer: FakePurchasesWriter,
    token_writer: FakeTokenWriter,
    token_reader: FakeTokenReader,
):
    TOKEN = PurchaseTokenDTO(1337, "abc")
    TOKEN_DATA = PurchaseTokenDataDTO(1337, "abc", datetime.now(), True, 100, 0)
    purchase_token_provider.purchase_token = TOKEN
    products_reader.products = [ProductDTO(1, 111, {"content": "content"})]
    token_reader.tokens = [TOKEN_DATA]
    token_writer.tokens = [TOKEN_DATA]

    handler = UsePurchaseTokenCMDHandler(
        uow,
        products_reader,
        purchase_token_provider,
        purchases_writer,
        token_writer,
        token_reader,
    )
    cmd = UsePurchaseTokenCMD(111, 101)

    with pytest.raises(TokenLimitExceeded) as exc_info:
        await handler(cmd)

    assert exc_info.value.params.get("available_to_buy") == 100

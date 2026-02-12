import pytest

from tests.unit.fake_adapters.customer_buys_products.products_reader import FakeProductsReader
from tests.unit.fake_adapters.customer_buys_products.purchases_writer import FakePurchasesWriter
from tests.unit.fake_adapters.customer_buys_products.token_reader import FakeTokenReader
from tests.unit.fake_adapters.customer_buys_products.token_writer import FakeTokenWriter
from tests.unit.fake_adapters.customer_buys_products.purchase_token_provider import FakePurchaseTokenProvider
from tests.unit.fake_adapters.customer_buys_products.products_writer import FakeProductsWriter


@pytest.fixture
def products_reader() -> FakeProductsReader:
    return FakeProductsReader()


@pytest.fixture
def purchase_token_provider() -> FakePurchaseTokenProvider:
    return FakePurchaseTokenProvider(None)


@pytest.fixture
def purchases_writer() -> FakePurchasesWriter:
    return FakePurchasesWriter()


@pytest.fixture
def token_writer() -> FakeTokenWriter:
    return FakeTokenWriter()


@pytest.fixture
def token_reader() -> FakeTokenReader:
    return FakeTokenReader()


@pytest.fixture
def products_writer() -> FakeProductsWriter:
    return FakeProductsWriter()

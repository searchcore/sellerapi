import pytest

from tests.unit.fake_adapters.admin_manages_products.products_writer import FakeProductsWriter


@pytest.fixture
def products_writer() -> FakeProductsWriter:
    return FakeProductsWriter()

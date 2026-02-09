import pytest

from .fake_adapters.common.uow import FakeUoW
from .fake_adapters.common.validators_provider import FakeValidatorProvider


@pytest.fixture
def uow() -> FakeUoW:
    return FakeUoW()


@pytest.fixture
def validator_provider() -> FakeValidatorProvider:
    return FakeValidatorProvider()

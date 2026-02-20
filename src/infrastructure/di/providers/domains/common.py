from dishka import Provider, Scope

from src.application.common.content_validators.default_validator import DefaultValidator
from src.application.common.interfaces import IUoW, IPurchaseTokenProvider, IValidatorProvider, ISchemaValidator

from src.infrastructure.implementations.common import UoW, PurchaseTokenProvider, ValidatorProvider, SchemaValidator

from src.infrastructure.implementations.common.purchase_token_provider import ScopedPurchaseToken

from src.infrastructure.validators_registry import ValidatorRegistry


def create_validator_registry() -> ValidatorRegistry:
    reg = ValidatorRegistry(DefaultValidator)
    reg.register_validators()

    return reg


def setup_provider(provider: Provider):
    provider.provide(UoW, scope=Scope.REQUEST, provides=IUoW)
    provider.provide(lambda: None, scope=Scope.REQUEST, provides=ScopedPurchaseToken)
    provider.provide(PurchaseTokenProvider, scope=Scope.REQUEST, provides=IPurchaseTokenProvider)
    provider.provide(create_validator_registry, scope=Scope.APP, provides=ValidatorRegistry)
    provider.provide(ValidatorProvider, scope=Scope.REQUEST, provides=IValidatorProvider)
    provider.provide(SchemaValidator, scope=Scope.APP, provides=ISchemaValidator)

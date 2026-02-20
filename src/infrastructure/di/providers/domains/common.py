from dishka import Provider, Scope

from src.application.common.interfaces import IUoW, IPurchaseTokenProvider, ISchemaValidator

from src.infrastructure.implementations.common import UoW, PurchaseTokenProvider, SchemaValidator

from src.infrastructure.implementations.common.purchase_token_provider import ScopedPurchaseToken


def setup_provider(provider: Provider):
    provider.provide(UoW, scope=Scope.REQUEST, provides=IUoW)
    provider.provide(lambda: None, scope=Scope.REQUEST, provides=ScopedPurchaseToken)
    provider.provide(PurchaseTokenProvider, scope=Scope.REQUEST, provides=IPurchaseTokenProvider)
    provider.provide(SchemaValidator, scope=Scope.APP, provides=ISchemaValidator)

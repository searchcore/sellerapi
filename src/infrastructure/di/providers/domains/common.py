from dishka import Provider, Scope

from src.application.common.interfaces import IUoW, IPurchaseTokenProvider, ISchemaValidator, IFeaturesReader

from src.infrastructure.implementations.common import UoW, PurchaseTokenProvider, SchemaValidator, FeaturesReader

from src.infrastructure.implementations.common.purchase_token_provider import ScopedPurchaseToken

from src.application.common.services import FeaturesService


def setup_services(provider: Provider):
    provider.provide(FeaturesService, scope=Scope.REQUEST, provides=FeaturesService)


def setup_provider(provider: Provider):
    provider.provide(UoW, scope=Scope.REQUEST, provides=IUoW)
    provider.provide(lambda: None, scope=Scope.REQUEST, provides=ScopedPurchaseToken)
    provider.provide(PurchaseTokenProvider, scope=Scope.REQUEST, provides=IPurchaseTokenProvider)
    provider.provide(SchemaValidator, scope=Scope.APP, provides=ISchemaValidator)
    provider.provide(FeaturesReader, scope=Scope.REQUEST, provides=IFeaturesReader)

    setup_services(provider)

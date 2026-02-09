from dishka import Provider, Scope

from src.application.customer_buys_products.commands.use_purchase_token import UsePurchaseTokenCMDHandler
from src.application.customer_buys_products.interfaces import (
    IProductsReader,
    IPurchasesWriter,
    ITokenReader,
    ITokenWriter,
    IProductsWriter,
)
from src.infrastructure.implementations.customer_buys_products import (
    ProductsReader,
    PurchasesWriter,
    TokenReader,
    TokenWriter,
    ProductsWriter,
)


def setup_provider(provider: Provider):
    provider.provide(ProductsReader, scope=Scope.REQUEST, provides=IProductsReader)
    provider.provide(PurchasesWriter, scope=Scope.REQUEST, provides=IPurchasesWriter)
    provider.provide(TokenReader, scope=Scope.REQUEST, provides=ITokenReader)
    provider.provide(TokenWriter, scope=Scope.REQUEST, provides=ITokenWriter)
    provider.provide(ProductsWriter, scope=Scope.REQUEST, provides=IProductsWriter)
    provider.provide(UsePurchaseTokenCMDHandler, scope=Scope.REQUEST, provides=UsePurchaseTokenCMDHandler)

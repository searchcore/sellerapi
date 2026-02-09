from dishka import Provider, Scope

from src.application.admin_manages_purchase_tokens.commands.increase_available_to_buy import IncreaseAvailableToBuyCMDHandler
from src.application.admin_manages_purchase_tokens.commands.create_token import CreatePurchaseTokenCMDHandler
from src.application.admin_manages_purchase_tokens.interfaces import IPurchaseTokensWriter, IPurchaseTokensReader
from src.infrastructure.implementations.admin_manages_purchase_tokens import PurchaseTokensWriter, PurchaseTokensReader


def setup_provider(provider: Provider):
    provider.provide(PurchaseTokensWriter, scope=Scope.REQUEST, provides=IPurchaseTokensWriter)
    provider.provide(PurchaseTokensReader, scope=Scope.REQUEST, provides=IPurchaseTokensReader)
    provider.provide(CreatePurchaseTokenCMDHandler, scope=Scope.REQUEST, provides=CreatePurchaseTokenCMDHandler)
    provider.provide(IncreaseAvailableToBuyCMDHandler, scope=Scope.REQUEST, provides=IncreaseAvailableToBuyCMDHandler)

from dishka import Provider, Scope

from src.application.admin_manages_products.commands.add_products_without_validation import AddProductsWithouValidationCMDHandler
from src.application.admin_manages_products.commands.add_products_with_validation import AddProductsWithValidationCMDHandler
from src.application.admin_manages_products.interfaces import IProductsWriter
from src.infrastructure.implementations.admin_manages_products import ProductsWriter


def setup_provider(provider: Provider):
    provider.provide(ProductsWriter, scope=Scope.REQUEST, provides=IProductsWriter)

    provider.provide(AddProductsWithouValidationCMDHandler, scope=Scope.REQUEST, provides=AddProductsWithouValidationCMDHandler)
    provider.provide(AddProductsWithValidationCMDHandler, scope=Scope.REQUEST, provides=AddProductsWithValidationCMDHandler)

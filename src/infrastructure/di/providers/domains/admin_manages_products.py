from dishka import Provider, Scope

from src.application.admin_manages_products.commands.add_products_without_validation import AddProductsWithouValidationCMDHandler
from src.application.admin_manages_products.commands.add_products_with_validation import AddProductsWithValidationCMDHandler
from src.application.admin_manages_products.commands.add_product_type import AddProductTypeCMDHandler
from src.application.admin_manages_products.interfaces import IProductsWriter, ISchemaWriter, ISchemaReader, IProductsReader
from src.infrastructure.implementations.admin_manages_products import ProductsWriter, SchemaWriter, SchemaReader, ProductsReader


def setup_provider(provider: Provider):
    provider.provide(ProductsWriter, scope=Scope.REQUEST, provides=IProductsWriter)
    provider.provide(SchemaWriter, scope=Scope.REQUEST, provides=ISchemaWriter)
    provider.provide(SchemaReader, scope=Scope.REQUEST, provides=ISchemaReader)
    provider.provide(ProductsReader, scope=Scope.REQUEST, provides=IProductsReader)

    provider.provide(AddProductTypeCMDHandler, scope=Scope.REQUEST, provides=AddProductTypeCMDHandler)
    provider.provide(AddProductsWithouValidationCMDHandler, scope=Scope.REQUEST, provides=AddProductsWithouValidationCMDHandler)
    provider.provide(AddProductsWithValidationCMDHandler, scope=Scope.REQUEST, provides=AddProductsWithValidationCMDHandler)

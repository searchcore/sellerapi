from dishka import Provider, Scope

from src.application.admin_manages_products.commands.import_products import ImportProductsCMDHandler
from src.application.admin_manages_products.commands.add_product_type import AddProductTypeCMDHandler
from src.application.admin_manages_products.queries.get_active_product_types import GetProductsTypesQRHandler
from src.application.admin_manages_products.queries.find_products import FindProductsQRHandler
from src.application.admin_manages_products.interfaces import IProductsWriter, ISchemaWriter, ISchemaReader, IProductsReader
from src.infrastructure.implementations.admin_manages_products import ProductsWriter, SchemaWriter, SchemaReader, ProductsReader


def setup_provider(provider: Provider):
    provider.provide(ProductsWriter, scope=Scope.REQUEST, provides=IProductsWriter)
    provider.provide(SchemaWriter, scope=Scope.REQUEST, provides=ISchemaWriter)
    provider.provide(SchemaReader, scope=Scope.REQUEST, provides=ISchemaReader)
    provider.provide(ProductsReader, scope=Scope.REQUEST, provides=IProductsReader)

    provider.provide(AddProductTypeCMDHandler, scope=Scope.REQUEST, provides=AddProductTypeCMDHandler)
    provider.provide(ImportProductsCMDHandler, scope=Scope.REQUEST, provides=ImportProductsCMDHandler)
    provider.provide(GetProductsTypesQRHandler, scope=Scope.REQUEST, provides=GetProductsTypesQRHandler)
    provider.provide(FindProductsQRHandler, scope=Scope.REQUEST, provides=FindProductsQRHandler)

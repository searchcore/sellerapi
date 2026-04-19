from dataclasses import dataclass

from src.application.common.request import Request, RequestHandler
from src.application.common.mediator import MR
from src.application.admin_manages_products.interfaces import IProductsReader
from src.application.admin_manages_products.dtos import ProductsTypesDTO


@dataclass(frozen=True)
class GetProductsTypesQR(Request[ProductsTypesDTO]):
    offset: int = 0
    limit: int = 100


@MR.register(GetProductsTypesQR)
class GetProductsTypesQRHandler(RequestHandler[GetProductsTypesQR, ProductsTypesDTO]):
    def __init__(self, products_reader: IProductsReader):
        self._products_reader = products_reader

    async def __call__(self, query: GetProductsTypesQR) -> ProductsTypesDTO:
        product_types = await self._products_reader.get_products_types(query.offset, query.limit)
        total = await self._products_reader.get_products_types_total()
        return ProductsTypesDTO(products_types=product_types, total=total)

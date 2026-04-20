from dataclasses import dataclass, field
from typing import Any

from src.domain.common.value_objects import ProductTypeIDVO
from src.application.common.request import Request, RequestHandler
from src.application.common.mediator import MR
from src.application.admin_manages_products.interfaces import IProductsReader
from src.application.admin_manages_products.dtos import FindProductsResultDTO


@dataclass(frozen=True)
class FindProductsQR(Request[FindProductsResultDTO]):
    product_type: ProductTypeIDVO
    contains: dict[str, Any] | None = field(default=None)


@MR.register(FindProductsQR)
class FindProductsQRHandler(RequestHandler[FindProductsQR, FindProductsResultDTO]):
    def __init__(self, products_reader: IProductsReader):
        self._products_reader = products_reader

    async def __call__(self, query: FindProductsQR) -> FindProductsResultDTO:
        products = await self._products_reader.find_products(
            product_type=query.product_type,
            contains=query.contains,
        )
        return FindProductsResultDTO(result=products)

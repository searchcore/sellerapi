from src.application.common.request import Request, RequestHandler
from dataclasses import dataclass

from src.application.common.mediator import MR
from src.application.common.interfaces import IUoW, IPurchaseTokenProvider

from src.application.customer_buys_products.interfaces import IProductsReader, ITokenReader


@dataclass(frozen=True)
class GetAvailableProductsCountQR(Request[int]):
    ...


@MR.register(GetAvailableProductsCountQR)
class GetAvailableProductsCountQRHandler(RequestHandler[GetAvailableProductsCountQR, int]):
    def __init__(
        self, 
        uow: IUoW, 
        products_reader: IProductsReader,
        purchase_token_provider: IPurchaseTokenProvider, 
        token_reader: ITokenReader,
    ):
        self._uow = uow
        self._products_reader = products_reader
        self._purchase_token_provider = purchase_token_provider
        self._token_reader = token_reader

    async def __call__(self, query: GetAvailableProductsCountQR) -> int:
        token = self._purchase_token_provider.get_token()
        token_data = await self._token_reader.get_token_data(token.id)

        return await self._products_reader.get_unsold_unreserved_products_count(token_data.product_type)

from src.application.common.request import Request, RequestHandler
from dataclasses import dataclass, field
from datetime import datetime

from src.application.common.mediator import MR
from src.application.common.interfaces import IUoW, IPurchaseTokenProvider
from src.application.common.services import FeaturesService

from src.application.customer_buys_products.interfaces import IProductsReader, ITokenReader


@dataclass(frozen=True)
class GetAvailableProductsCountQR(Request[int]):
    with_features: list[str] | None = None
    since: datetime | None = field(default=None)
    until: datetime | None = field(default=None)


@MR.register(GetAvailableProductsCountQR)
class GetAvailableProductsCountQRHandler(RequestHandler[GetAvailableProductsCountQR, int]):
    def __init__(
        self, 
        uow: IUoW, 
        products_reader: IProductsReader,
        purchase_token_provider: IPurchaseTokenProvider, 
        token_reader: ITokenReader,
        features_service: FeaturesService,
    ):
        self._uow = uow
        self._products_reader = products_reader
        self._purchase_token_provider = purchase_token_provider
        self._token_reader = token_reader
        self._features_service = features_service

    async def __call__(self, query: GetAvailableProductsCountQR) -> int:
        token = self._purchase_token_provider.get_token()
        token_data = await self._token_reader.get_token_data(token.id)

        feature_ids = []
        if query.with_features:
            feature_ids = await self._features_service.get_ids_by_codes(token_data.product_type, query.with_features)

        return await self._products_reader.get_unsold_unreserved_products_count(token_data.product_type, feature_ids, query.since, query.until)

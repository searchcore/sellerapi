from src.application.common.request import Request, RequestHandler
from dataclasses import dataclass
import logging

from src.application.common.dtos import NewProductDTO
from src.application.common.mediator import MR
from src.application.common.interfaces import IUoW

from src.application.admin_manages_products.interfaces import IProductsWriter


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class AddProductsWithoutValidationCMD(Request[None]):
    products: list[NewProductDTO]


@MR.register(AddProductsWithoutValidationCMD)
class AddProductsWithouValidationCMDHandler(RequestHandler[AddProductsWithoutValidationCMD, None]):
    def __init__(self, uow: IUoW, products_writer: IProductsWriter):
        self._uow = uow
        self._products_writer = products_writer

    async def __call__(self, cmd: AddProductsWithoutValidationCMD) -> None:
        await self._products_writer.add_products(cmd.products)
        await self._uow.commit()

        logger.info(
            "products_added_without_validation",
            extra={
                "added": len(cmd.products),
            }
        )

from src.application.common.request import Request, RequestHandler
from dataclasses import dataclass
import logging

from src.application.common.content_validators.abc import IdentifiedProduct
from src.application.common.dtos import NewProductDTO
from src.application.common.mediator import MR
from src.application.common.interfaces import IUoW, IValidatorProvider

from src.application.admin_manages_products.dtos import AddProductsResultDTO
from src.application.admin_manages_products.interfaces import IProductsWriter


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class AddProductsWithValidationCMD(Request[AddProductsResultDTO]):
    product_type: int
    products: list[NewProductDTO]


@MR.register(AddProductsWithValidationCMD)
class AddProductsWithValidationCMDHandler(RequestHandler[AddProductsWithValidationCMD, AddProductsResultDTO]):
    def __init__(self, uow: IUoW, products_writer: IProductsWriter, validator_provider: IValidatorProvider):
        self._uow = uow
        self._products_writer = products_writer
        self._validator_provider = validator_provider

    async def __call__(self, cmd: AddProductsWithValidationCMD) -> AddProductsResultDTO:
        validator = self._validator_provider.get_validator(cmd.product_type)

        products_with_id = [IdentifiedProduct(i, p.content) for i, p in enumerate(cmd.products)]
        validation_reports = await validator.batch_validate(products_with_id, concurrency=100)

        valid_products = [cmd.products[report.product_id] for report in validation_reports if report.product_valid]

        if valid_products:
            await self._products_writer.add_products(valid_products)
            await self._uow.commit()
        
        logger.info(
            "products_added_with_validation",
            extra={
                "product_type": cmd.product_type,
                "added": len(valid_products),
                "requested_to_add": len(cmd.products),
            }
        )

        return AddProductsResultDTO(
            len(valid_products),
            [report for report in validation_reports if not report.product_valid]
        )

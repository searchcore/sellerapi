from src.application.common.request import Request, RequestHandler
from dataclasses import dataclass
import logging

from src.domain.common.value_objects import ProductTypeSchemaVersionVO, ProductTypeIDVO
from src.application.common.dtos import NewProductDTO
from src.application.common.mediator import MR
from src.application.common.interfaces import IUoW, ISchemaValidator
from src.application.common.interfaces.schema_validator import ContentValidationReport
from src.application.common.exceptions import ProductTypeSchemaNotFound, ProductTypeNotFound

from src.application.admin_manages_products.dtos import AddProductsResultDTO
from src.application.admin_manages_products.interfaces import IProductsWriter, ISchemaReader, IProductsReader


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class AddProductsWithValidationCMD(Request[AddProductsResultDTO]):
    product_type: ProductTypeIDVO
    products: list[NewProductDTO]
    schema_version: ProductTypeSchemaVersionVO | None = None


@MR.register(AddProductsWithValidationCMD)
class AddProductsWithValidationCMDHandler(RequestHandler[AddProductsWithValidationCMD, AddProductsResultDTO]):
    def __init__(
        self,
        uow: IUoW,
        products_writer: IProductsWriter,
        schema_validator: ISchemaValidator,
        schema_reader: ISchemaReader,
        products_reader: IProductsReader,
    ):
        self._uow = uow
        self._products_writer = products_writer
        self._products_reader = products_reader
        self._schema_validator = schema_validator
        self._schema_reader = schema_reader

    async def __call__(self, cmd: AddProductsWithValidationCMD) -> AddProductsResultDTO:
        if not await self._products_reader.does_product_type_exist(cmd.product_type):
            raise ProductTypeNotFound(f"Product type {cmd.product_type.value} does not exist.")

        if cmd.schema_version is not None:
            product_type_schema = await self._schema_reader.get_schema_for_product_type_and_version(cmd.product_type, cmd.schema_version)

            if product_type_schema is None:
                raise ProductTypeSchemaNotFound(
                    f"Provided schema with version {cmd.schema_version.value} "
                    f"not found for product type {cmd.product_type.value}."
                )
        else:
            product_type_schema = await self._schema_reader.get_schema_with_biggest_version(cmd.product_type)

        validation_reports: list[ContentValidationReport] = []

        for product in cmd.products:
            report = self._schema_validator.validate_content(product.content, product_type_schema.schema)
            validation_reports.append(report)

        valid_products = [
            cmd.products[product_id]
            for product_id, report 
            in enumerate(validation_reports) 
            if report.product_valid
        ]

        if valid_products:
            await self._products_writer.add_products(product_type_schema.id, valid_products)
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

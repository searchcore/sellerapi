from src.application.common.request import Request, RequestHandler
from dataclasses import dataclass
import logging

from src.domain.common.value_objects import ProductTypeIDVO, ProductTypeSchemaVO, ProductTypeSchemaVersionVO

from src.application.common.mediator import MR
from src.application.common.interfaces import IUoW, ISchemaValidator

from src.application.admin_manages_products.interfaces import IProductsWriter, ISchemaWriter
from src.application.common.exceptions import ProductTypeSchemaInvalid

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class AddProductTypeCMD(Request[ProductTypeIDVO]):
    name: str
    schema: ProductTypeSchemaVO


@MR.register(AddProductTypeCMD)
class AddProductTypeCMDHandler(RequestHandler[AddProductTypeCMD, ProductTypeIDVO]):
    def __init__(
        self,
        uow: IUoW,
        products_writer: IProductsWriter,
        schema_validator: ISchemaValidator,
        schema_writer: ISchemaWriter
    ):
        self._uow = uow
        self._products_writer = products_writer
        self._schema_validator = schema_validator
        self._schema_writer = schema_writer

    async def __call__(self, cmd: AddProductTypeCMD) -> ProductTypeIDVO:
        type_id = await self._products_writer.add_product_type(cmd.name)

        if not self._schema_validator.is_schema_valid(cmd.schema):
            raise ProductTypeSchemaInvalid("Provided product type schema is invalid!")

        schema_type_id = await self._schema_writer.add_product_type_schema(type_id, ProductTypeSchemaVersionVO(1), cmd.schema)

        await self._uow.commit()

        logger.info(
            "new_product_type_created",
            extra={
                "product_type_id": type_id.value,
                "product_type_name": cmd.name,
                "product_type_schema_id": schema_type_id.value,
            }
        )

        return type_id

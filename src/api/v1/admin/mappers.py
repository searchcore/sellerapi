from src.application.admin_manages_purchase_tokens.commands import CreatePurchaseTokenCMD, IncreaseAvailableToBuyCMD
from src.application.admin_manages_products.commands import AddProductsWithoutValidationCMD, AddProductsWithValidationCMD, AddProductTypeCMD

from src.domain.common.value_objects import (
    ProductTypeIDVO,
    ProductTypeSchemaVO,
)

from src.application.common.dtos import NewProductDTO
from src.application.admin_manages_purchase_tokens.dtos import CreatedTokenDTO
from src.application.admin_manages_products.dtos import AddProductsResultDTO

from .schemas import (
    AddProductsWithoutValidationRequest,
    AddProductsWithValidationRequest,
    CreatePurchaseTokenRequest,
    CreatedTokenResponse,
    AddedProductsValidatedResponse,
    ValidationReportResponse,
    ValidationExecutionErrorResponse,
    ValidationErrorResponse,
    AddProductTypeRequest,
    CreatedProductTypeResponse,
)


def dto_to_resp_created_token(dto: CreatedTokenDTO) -> CreatedTokenResponse:
    return CreatedTokenResponse(token_id=dto.token_id, secret_token=dto.token)


def dto_to_resp_added_products_validated(dto: AddProductsResultDTO) -> AddedProductsValidatedResponse:
    return AddedProductsValidatedResponse(
        added=dto.added_products_amount,
        invalid=[
            ValidationReportResponse(
                id=product_id,
                violations=[ValidationErrorResponse(message=e.details, params=e.params) for e in report.violations],
                execution_error=ValidationExecutionErrorResponse(
                    message=report.execution_error.details,
                    params=report.execution_error.params
                ) if report.execution_error else None
            )
            for product_id, report
            in enumerate(dto.not_added_products)
        ]
    )


def req_to_cmd_create_purchase_token(req: CreatePurchaseTokenRequest) -> CreatePurchaseTokenCMD:
    return CreatePurchaseTokenCMD(req.expires_at, req.available_to_buy)


def req_to_cmd_increase_available_to_buy(token_id: int, amount: int) -> IncreaseAvailableToBuyCMD:
    return IncreaseAvailableToBuyCMD(token_id, amount)


def req_to_cmd_add_prod_without_validation(req: AddProductsWithoutValidationRequest) -> AddProductsWithoutValidationCMD:
    return AddProductsWithoutValidationCMD(
        products=[
            NewProductDTO(
                req.product_type,
                p,
            )
            for p
            in req.products
        ]
    )


def req_to_cmd_add_prod_with_validation(req: AddProductsWithValidationRequest) -> AddProductsWithValidationCMD:
    return AddProductsWithValidationCMD(
        product_type=ProductTypeIDVO(req.product_type),
        products=[
            NewProductDTO(
                req.product_type,
                p,
            )
            for p
            in req.products
        ]
    )


def req_to_cmd_add_prod_type(req: AddProductTypeRequest) -> AddProductTypeCMD:
    return AddProductTypeCMD(
        name=req.name,
        schema=ProductTypeSchemaVO(req.content_schema)
    )


def vo_to_resp_created_prod_type(vo: ProductTypeIDVO) -> CreatedProductTypeResponse:
    return CreatedProductTypeResponse(product_type_id=vo.value)

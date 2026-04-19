from datetime import datetime
from pydantic import BaseModel
from typing import Any


class CreatePurchaseTokenRequest(BaseModel):
    product_type: int
    expires_at: datetime
    available_to_buy: int


class ImportProductsRequest(BaseModel):
    product_type: int
    products: list[dict[str, Any]]
    with_features: list[str] | None = None


class AddProductTypeRequest(BaseModel):
    name: str
    content_schema: dict[str, Any]


class ValidationExecutionErrorResponse(BaseModel):
    message: str
    params: dict[str, Any]


class ValidationErrorResponse(BaseModel):
    message: str
    params: dict[str, Any]


class ValidationReportResponse(BaseModel):
    id: int
    violations: list[ValidationErrorResponse]
    execution_error: ValidationExecutionErrorResponse | None


class ImportedProductsResponse(BaseModel):
    added: int
    invalid: list[ValidationReportResponse]


class CreatedTokenResponse(BaseModel):
    token_id: int
    secret_token: str


class CreatedProductTypeResponse(BaseModel):
    product_type_id: int


class CurrentSchemaResponse(BaseModel):
    id: int
    version: int
    product_schema: dict[str, Any]


class ProductTypeResponse(BaseModel):
    id: int
    name: str
    current_schema: CurrentSchemaResponse


class ProductsTypesResponse(BaseModel):
    products_types: list[ProductTypeResponse]
    total: int

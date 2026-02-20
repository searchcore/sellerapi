from fastapi import APIRouter, Depends, Query
from src.core.responses import SuccessResponse, success, success_empty, EmptyResponse
from src.api.deps import get_mediator, get_access_token
from src.application.common.mediator import Mediator
from src.application.common.dtos import AccessTokenBriefDTO

from typing import Annotated

from .schemas import (
    ImportProductsRequest,
    CreatePurchaseTokenRequest,
    CreatedTokenResponse,
    ImportedProductsResponse,
    AddProductTypeRequest,
    CreatedProductTypeResponse,
)
from .mappers import (
    dto_to_resp_imported_products,
    dto_to_resp_created_token,
    req_to_cmd_create_purchase_token,
    req_to_cmd_increase_available_to_buy,
    req_to_cmd_import_products,
    req_to_cmd_add_prod_type,
    vo_to_resp_created_prod_type,
)

router = APIRouter()


@router.post(
    "/tokens/purchase",
    response_model=SuccessResponse[CreatedTokenResponse],
)
async def create_token(
    body: CreatePurchaseTokenRequest,
    mediator: Mediator = Depends(get_mediator),
    token: AccessTokenBriefDTO = Depends(get_access_token),
):
    cmd = req_to_cmd_create_purchase_token(body)
    purchase_token = await mediator.send(cmd)

    return success(dto_to_resp_created_token(purchase_token))


@router.post(
    "/tokens/purchase/{token_id}/increase_available_to_buy",
    response_model=SuccessResponse[EmptyResponse],
)
async def increase_available_to_buy(
    token_id: int,
    amount: Annotated[int, Query(title="Amount to add to current limit", ge=1)],
    mediator: Mediator = Depends(get_mediator),
    token: AccessTokenBriefDTO = Depends(get_access_token),
):
    cmd = req_to_cmd_increase_available_to_buy(token_id, amount)
    await mediator.send(cmd)

    return success_empty()


@router.post(
    "/products/import",
    response_model=SuccessResponse[ImportedProductsResponse],
)
async def import_products(
    body: ImportProductsRequest,
    mediator: Mediator = Depends(get_mediator),
    token: AccessTokenBriefDTO = Depends(get_access_token),
):
    cmd = req_to_cmd_import_products(body)
    result = await mediator.send(cmd)

    return success(
        dto_to_resp_imported_products(result)
    )


@router.post(
    "/products/type",
    response_model=SuccessResponse[CreatedProductTypeResponse],
)
async def create_product_type(
    body: AddProductTypeRequest,
    mediator: Mediator = Depends(get_mediator),
    token: AccessTokenBriefDTO = Depends(get_access_token),
):
    cmd = req_to_cmd_add_prod_type(body)
    result = await mediator.send(cmd)

    return success(
        vo_to_resp_created_prod_type(result)
    )

from fastapi import APIRouter, Depends, Query
from src.core.responses import SuccessResponse, success, success_empty, EmptyResponse
from src.api.deps import get_mediator, get_access_token
from src.application.common.mediator import Mediator
from src.application.common.dtos import AccessTokenBriefDTO

from typing import Annotated

from .schemas import (
    AddProductsWithValidationRequest,
    AddProductsWithoutValidationRequest,
    CreatePurchaseTokenRequest,
    CreatedTokenResponse,
    AddedProductsValidatedResponse,
)
from .mappers import (
    dto_to_resp_added_products_validated,
    dto_to_resp_created_token,
    req_to_cmd_create_purchase_token,
    req_to_cmd_increase_available_to_buy,
    req_to_cmd_add_prod_without_validation,
    req_to_cmd_add_prod_with_validation,
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
    response_model=SuccessResponse[EmptyResponse],
)
async def import_products(
    body: AddProductsWithoutValidationRequest,
    mediator: Mediator = Depends(get_mediator),
    token: AccessTokenBriefDTO = Depends(get_access_token),
):
    cmd = req_to_cmd_add_prod_without_validation(body)
    await mediator.send(cmd)

    return success_empty()


@router.post(
    "/products/import/validate",
    response_model=SuccessResponse[AddedProductsValidatedResponse],
)
async def import_products_with_validation(
    body: AddProductsWithValidationRequest,
    mediator: Mediator = Depends(get_mediator),
    token: AccessTokenBriefDTO = Depends(get_access_token),
):
    cmd = req_to_cmd_add_prod_with_validation(body)
    result = await mediator.send(cmd)

    return success(
        dto_to_resp_added_products_validated(result)
    )

from fastapi import APIRouter, Depends, Query
from src.core.responses import SuccessResponse, success
from src.api.deps import get_purchase_token_ctx, get_mediator
from src.application.common.mediator import Mediator
from src.application.customer_buys_products.commands.use_purchase_token import UsePurchaseTokenCMD
from src.infrastructure.implementations.common.purchase_token_provider import ScopedPurchaseToken
from src.application.common.dtos.purchase_token import PurchaseTokenDTO

from typing import Any, Annotated


from .schemas import (
    PurchaseProductsResponse,
)
from .mappers import (
    dto_to_resp_purchase_products,
)


router = APIRouter()


def include_fields(fields: list[str], data: dict[Any, Any]):
    return { key: data[key] for key in fields if key in data} or data


@router.post(
    "/products/purchase/token",
    response_model=SuccessResponse[PurchaseProductsResponse]
)
async def purchase_products(
    type: int,
    fields: Annotated[list[str] | None, Query()] = None,
    amount: Annotated[int, Query(title="Amount of products to purchase", ge=1, le=500)] = 1,
    purchase_token: PurchaseTokenDTO = Depends(get_purchase_token_ctx),
    mediator: Mediator = Depends(get_mediator),
):
    cmd = UsePurchaseTokenCMD(type, amount)
    products = await mediator.send(cmd, context={ScopedPurchaseToken: purchase_token})

    resp = dto_to_resp_purchase_products(products)
    if fields:
        resp.products = [include_fields(fields, p) for p in resp.products]

    return success(resp)

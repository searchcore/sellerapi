from fastapi import status, Header, Query
from dishka.integrations.fastapi import (
    FromDishka,
    inject,
)

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.exceptions import PurchaseTokenMissing, PurchaseTokenInvalid
from src.application.common.dtos import PurchaseTokenDTO

from src.infrastructure.adapters.purchase_token_reader import (
    PurchaseTokenReader,
)


@inject
async def get_purchase_token_ctx(
    session: FromDishka[AsyncSession],
    purchase_token: str | None = Query(None),
    x_purchase_token: str | None = Header(None)
) -> PurchaseTokenDTO:
    if not (purchase_token or x_purchase_token):
        raise PurchaseTokenMissing(
            "You must provide either X-Purchase-Token header or purchase_token query parameter.",
            status_code=status.HTTP_403_FORBIDDEN,
        )

    purchase_token = purchase_token or x_purchase_token

    reader = PurchaseTokenReader(session)
    token_obj = await reader.get(purchase_token)

    if token_obj is None:
        raise PurchaseTokenInvalid(
            "Invalid token",
            status_code=status.HTTP_403_FORBIDDEN,
        )

    return token_obj

from src.application.customer_buys_products.interfaces import ITokenReader

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import PurchaseTokenModel
from src.application.common.exceptions import PurchaseTokenNotFound
from src.application.common.dtos.purchase_token_data import PurchaseTokenDataDTO

from src.domain.common.value_objects import ProductTypeIDVO


class TokenReader(ITokenReader):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_token_data(self, token_id: int) -> PurchaseTokenDataDTO:
        model = await self._session.get(PurchaseTokenModel, token_id)

        if model is None:
            raise PurchaseTokenNotFound(f"Provided token does not exist!")
    
        return PurchaseTokenDataDTO(
            model.id,
            ProductTypeIDVO(model.product_type),
            model.expires_at,
            model.is_active,
            model.available_to_buy,
            model.used_count,
        )

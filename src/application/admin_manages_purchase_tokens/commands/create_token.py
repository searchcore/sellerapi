from src.application.common.request import Request, RequestHandler
from dataclasses import dataclass
from datetime import datetime
import secrets
import logging

from src.domain.common.value_objects import ProductTypeIDVO
from src.application.common.mediator import MR
from src.application.common.interfaces import IUoW

from src.application.admin_manages_purchase_tokens.interfaces import IPurchaseTokensWriter
from src.application.admin_manages_purchase_tokens.dtos import CreatedTokenDTO


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class CreatePurchaseTokenCMD(Request[CreatedTokenDTO]):
    product_type: ProductTypeIDVO
    expires_at: datetime
    available_to_buy: int


@MR.register(CreatePurchaseTokenCMD)
class CreatePurchaseTokenCMDHandler(RequestHandler[CreatePurchaseTokenCMD, CreatedTokenDTO]):
    def __init__(self, uow: IUoW, purchase_tokens_writer: IPurchaseTokensWriter):
        self._uow = uow
        self._purchase_tokens_writer = purchase_tokens_writer

    async def __call__(self, cmd: CreatePurchaseTokenCMD) -> CreatedTokenDTO:
        token = secrets.token_urlsafe(32)

        token_id = await self._purchase_tokens_writer.add_token(cmd.product_type, token, cmd.expires_at, cmd.available_to_buy)

        await self._uow.commit()

        logger.info(
            "purchase_token_created",
            extra={
                "product_type": cmd.product_type.value,
                "token_id": token_id,
                "expires_at": cmd.expires_at,
                "available_to_buy": cmd.available_to_buy,
            }
        )

        return CreatedTokenDTO(token_id, token)

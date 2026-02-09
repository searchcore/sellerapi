from src.application.common.request import Request, RequestHandler
from dataclasses import dataclass
import logging

from src.application.common.mediator import MR
from src.application.common.interfaces import IUoW

from src.application.admin_manages_purchase_tokens.interfaces import IPurchaseTokensWriter, IPurchaseTokensReader

from src.application.common.exceptions import PurchaseTokenNotFound


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class IncreaseAvailableToBuyCMD(Request[None]):
    token_id: int
    to_add: int


@MR.register(IncreaseAvailableToBuyCMD)
class IncreaseAvailableToBuyCMDHandler(RequestHandler[IncreaseAvailableToBuyCMD, None]):
    def __init__(self, uow: IUoW, purchase_tokens_writer: IPurchaseTokensWriter, purchase_tokens_reader: IPurchaseTokensReader):
        self._uow = uow
        self._purchase_tokens_writer = purchase_tokens_writer
        self._purchase_tokens_reader = purchase_tokens_reader

    async def __call__(self, cmd: IncreaseAvailableToBuyCMD) -> str:
        if not await self._purchase_tokens_reader.is_token_exist(cmd.token_id):
            raise PurchaseTokenNotFound("Provided token does not exist!")

        await self._purchase_tokens_writer.add_to_available_to_buy(cmd.token_id, cmd.to_add)

        await self._uow.commit()

        logger.info(
            "purchase_token_increased_available_to_buy",
            extra={
                "token_id": cmd.token_id,
                "added": cmd.to_add,
            }
        )

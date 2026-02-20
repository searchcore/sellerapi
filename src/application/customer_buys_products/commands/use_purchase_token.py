from src.application.common.request import Request, RequestHandler
from dataclasses import dataclass, field
import logging

from src.application.common.exceptions import ProductOutOfStock
from src.application.common.mediator import MR
from src.application.common.interfaces import IUoW, IPurchaseTokenProvider

from src.application.customer_buys_products.exceptions import TokenLimitExceeded
from src.application.customer_buys_products.interfaces import IProductsReader, IPurchasesWriter, ITokenWriter, ITokenReader, IProductsWriter

from src.application.common.dtos import NewPurchaseDTO, ProductDTO


@dataclass(frozen=True)
class UsePurchaseTokenCMD(Request[list[ProductDTO]]):
    amount: int
    clear_content: bool = field(default=False)


@MR.register(UsePurchaseTokenCMD)
class UsePurchaseTokenCMDHandler(RequestHandler[UsePurchaseTokenCMD, list[ProductDTO]]):
    def __init__(
        self, 
        uow: IUoW, 
        products_reader: IProductsReader,
        purchase_token_provider: IPurchaseTokenProvider, 
        purchases_writer: IPurchasesWriter, 
        token_writer: ITokenWriter,
        token_reader: ITokenReader,
        products_writer: IProductsWriter,
    ):
        self._uow = uow
        self._products_reader = products_reader
        self._purchase_token_provider = purchase_token_provider
        self._purchases_writer = purchases_writer
        self._token_writer = token_writer
        self._token_reader = token_reader
        self._products_writer = products_writer

    async def __call__(self, cmd: UsePurchaseTokenCMD) -> list[ProductDTO]:
        token = self._purchase_token_provider.get_token()
        token_data = await self._token_reader.get_token_data(token.id)

        if cmd.amount > token_data.available_to_buy:
            raise TokenLimitExceeded(
                "Your request exceeds your token limits. "
                f"Currently you can get {token_data.available_to_buy} products, but {cmd.amount} requested. "
                "Please, ask administrator to increase token limits, get new token or lower your amount.",
                params={
                    "available_to_buy": token_data.available_to_buy
                }
            )

        products = await self._products_reader.get_unsold_unreserved_products(token_data.product_type.value, cmd.amount)

        if len(products) != cmd.amount:
            raise ProductOutOfStock(
                f"Requested product amount is out of stock! Please, try again later.",
                params={
                    "available": len(products),
                }
            )

        await self._purchases_writer.add_purchases([NewPurchaseDTO(token.id, p.id) for p in products])
        await self._token_writer.add_to_used_count(token.id, len(products))
        await self._token_writer.sub_available_to_buy(token.id, len(products))

        if cmd.clear_content:
            await self._products_writer.set_content(products, {})

        await self._uow.commit()
    
        logging.info(
            "purchase_token_used",
            extra={
                "token_id": token_data.id,
                "amount": len(products),
            }
        )

        return products

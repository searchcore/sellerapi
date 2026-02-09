from src.application.common.dtos import ProductDTO

from .schemas import (
    PurchaseProductsResponse,
)


def dto_to_resp_purchase_products(dtos: list[ProductDTO]) -> PurchaseProductsResponse:
    return PurchaseProductsResponse(
        products=[
            p.content
            for p
            in dtos
        ]
    )

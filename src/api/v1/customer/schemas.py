from pydantic import BaseModel
from typing import Any


class PurchaseProductsResponse(BaseModel):
    products: list[dict[Any, Any]]

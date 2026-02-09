from dataclasses import dataclass
from typing import Any, Any


@dataclass(frozen=True)
class NewProductDTO:
    product_type_id: int
    content: dict[Any, Any]

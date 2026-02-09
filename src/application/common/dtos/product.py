from dataclasses import dataclass
from typing import Any, Any


@dataclass(frozen=True)
class ProductDTO:
    id: int
    type: int
    content: dict[Any, Any]

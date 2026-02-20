from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ProductTypeSchemaVO:
    value: dict[str, Any]

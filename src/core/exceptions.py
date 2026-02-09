from enum import StrEnum
from typing import Any, ClassVar
from dataclasses import dataclass, field


class ErrorCodes(StrEnum):
    UNEXPECTED = "unexpected"
    BAD_AUTH = "bad_auth"
    PURCHASE_TOKEN_NOT_FOUND = "purchase_token_not_found"
    PRODUCT_OUT_OF_STOCK = "product_out_of_stock"
    TOKEN_LIMIT_EXCEEDED = "token_limit_exceeded"


@dataclass(eq=False)
class BaseAppException(Exception):
    code: ClassVar[ErrorCodes] = None

    details: str
    params: dict[str, Any] = field(default_factory=dict)

    def __init_subclass__(cls):
        if cls.code is None:
            raise TypeError(
                f"{cls.__name__} must define code"
            )

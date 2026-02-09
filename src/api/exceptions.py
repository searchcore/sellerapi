from dataclasses import dataclass
from enum import StrEnum
from typing import ClassVar
from src.core.exceptions import BaseAppException, ErrorCodes


class APIErrorCodes(StrEnum):
    PURCHASE_TOKEN_MISSING = "purchase_token_missing"
    PURCHASE_TOKEN_INVALID = "purchase_token_invalid"


@dataclass(eq=False)
class APIError(BaseAppException):
    code: ClassVar[APIErrorCodes | ErrorCodes] = ErrorCodes.UNEXPECTED
    status_code: int = 400


class BadAuth(APIError):
    code = ErrorCodes.BAD_AUTH


class PurchaseTokenMissing(APIError):
    code = APIErrorCodes.PURCHASE_TOKEN_MISSING


class PurchaseTokenInvalid(APIError):
    code = APIErrorCodes.PURCHASE_TOKEN_INVALID

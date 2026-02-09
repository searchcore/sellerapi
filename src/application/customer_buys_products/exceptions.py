from src.core.exceptions import BaseAppException, ErrorCodes


class TokenLimitExceeded(BaseAppException):
    code = ErrorCodes.TOKEN_LIMIT_EXCEEDED

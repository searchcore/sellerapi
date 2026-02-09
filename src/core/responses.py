from typing import TypeVar, Generic, Any, Literal, Type
from pydantic import BaseModel, create_model

from src.core.exceptions import BaseAppException

T = TypeVar("T")


class SuccessResponse(BaseModel, Generic[T]):
    data: T


class ErrorResponse(BaseModel, Generic[T]):
    error: T


# proper way would be manual responses writing
# but for now its a bit tedious
# main issues with such mapper are:
# - unintentional changes in docs when changing inner application error
# - poor openapi naming like ErrorResponse_PurchaseTokenNotFoundResponse_
# - even more poor naming when exceptions have same names (pydantic adds extra info to classname)
# but for now i think its ok
def create_error_resp(exc_cls: Type[BaseAppException]) -> Type[ErrorResponse]:
    name = f"{exc_cls.__name__}Response"

    Error = create_model(
        name,
        code=(Literal[exc_cls.code], exc_cls.code),
        details=(str, ...),
        params=(dict[str, Any], {})
    )
    return ErrorResponse[Error]


def success(response: T) -> SuccessResponse[T]:
    return SuccessResponse(data=response)


class EmptyResponse(BaseModel):
    ...


def success_empty() -> SuccessResponse[EmptyResponse]:
    return SuccessResponse(data=EmptyResponse())

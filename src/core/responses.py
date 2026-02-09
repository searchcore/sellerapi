from typing import TypeVar, Generic
from pydantic import BaseModel


T = TypeVar("T")


class SuccessResponse(BaseModel, Generic[T]):
    data: T


class ErrorResponse(BaseModel):
    error: str


def success(response: T) -> SuccessResponse[T]:
    return SuccessResponse(data=response)


class EmptyResponse(BaseModel):
    ...


def success_empty() -> SuccessResponse[EmptyResponse]:
    return SuccessResponse(data=EmptyResponse())

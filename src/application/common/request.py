from typing import Generic, TypeVar, Any
from abc import ABC, abstractmethod
from dataclasses import dataclass


R = TypeVar("R")


@dataclass(frozen=True)
class Request(ABC, Generic[R]):
    pass


RQ = TypeVar("RQ", bound=Request[Any])


class RequestHandler(ABC, Generic[RQ, R]):
    @abstractmethod
    async def __call__(self, request: RQ) -> R:
        pass

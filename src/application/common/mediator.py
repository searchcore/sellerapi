from .request import Request, RequestHandler
from typing import Any, TypeVar
from types import TracebackType
from abc import ABC, abstractmethod


class IScopedHandlersContainer(ABC):
    @abstractmethod
    async def get_handler(self, handler_t: type) -> Any:
        ...

    async def __aenter__(self) -> "IScopedHandlersContainer":
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc_val: BaseException | None = None,
        exc_tb: TracebackType | None = None
    ) -> None:
        ...

class IHandlersContainer(ABC):
    def __call__(self, *args, **kwargs) -> IScopedHandlersContainer:
        ...


H = TypeVar("H")


class RequestHandlersRegistry:
    def __init__(self):
        self._map: dict[type[Request], type[RequestHandler]] = {}

    def register(self, request_type: type[Request]):
        def wrapper(handler_cls: type[H]) -> type[H]:
            self._map[request_type] = handler_cls
            return handler_cls
        return wrapper

    @property
    def map(self):
        return self._map

GLOBAL_HANDLERS_REGISTRY = RequestHandlersRegistry()
MR = GLOBAL_HANDLERS_REGISTRY

R = TypeVar("R")


class Mediator:
    def __init__(self, registry: RequestHandlersRegistry):
        self._registry = registry
        self._container: IHandlersContainer | None = None
    
    def set_container(self, container: IHandlersContainer):
        self._container = container

    async def send(self, request: Request[R], *, context: dict[Any, Any] | None = None) -> R:
        handler_t = self._registry.map[type(request)]
        async with self._container(context) as container:
            handler = await container.get_handler(handler_t)
            return await handler(request)

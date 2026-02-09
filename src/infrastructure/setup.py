from dishka import AsyncContainer
from dishka.async_container import AsyncContextWrapper
from typing import Any
from types import TracebackType

from src.application.common.mediator import Mediator, IHandlersContainer, IScopedHandlersContainer, GLOBAL_HANDLERS_REGISTRY

from src.infrastructure.di.setup import setup_di


class ScopedHandlersContainer(IScopedHandlersContainer):
    def __init__(self, context_wrapper: AsyncContextWrapper):
        self._context_wrapper = context_wrapper
        self._container: AsyncContainer | None = None
 
    async def get_handler(self, handler_t: type) -> Any:
        return await self._container.get(handler_t)

    async def __aenter__(self) -> "IScopedHandlersContainer":
        self._container = await self._context_wrapper.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc_val: BaseException | None = None,
        exc_tb: TracebackType | None = None
    ) -> None:
        return await self._context_wrapper.__aexit__(exc_type, exc_val, exc_tb)


class HandlersContainer(IHandlersContainer):
    def __init__(self, container: AsyncContainer):
        self._container = container

    def __call__(self, *args, **kwargs) -> "IScopedHandlersContainer":
        return ScopedHandlersContainer(self._container.__call__(*args, **kwargs))


def setup_infrastructure() -> AsyncContainer:
    mediator = Mediator(GLOBAL_HANDLERS_REGISTRY)
    container = setup_di()
    handlers_container = HandlersContainer(container)
    mediator.set_container(handlers_container)

    return container


def setup_mediator(container: AsyncContainer) -> Mediator:
    mediator = Mediator(GLOBAL_HANDLERS_REGISTRY)
    handlers_container = HandlersContainer(container)
    mediator.set_container(handlers_container)

    return mediator

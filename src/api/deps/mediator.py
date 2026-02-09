from fastapi import Request

from src.application.common.mediator import Mediator


def get_mediator(request: Request) -> Mediator:
    return request.app.state.mediator

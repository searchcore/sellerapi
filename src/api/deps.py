import hashlib

from fastapi import Request, Header, status
from dishka.integrations.fastapi import (
    FromDishka,
    inject,
)

from src.api.exceptions import BadAuth

from src.application.common.mediator import Mediator

from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.adapters.access_token_reader import AccessTokenReader


def hash_token(access_token_raw: str) -> str:
    return hashlib.sha256(access_token_raw.encode()).hexdigest()


@inject
async def get_token(
    session: FromDishka[AsyncSession],
    authorization: str = Header(...)
):
    if not authorization.startswith("Bearer "):
        raise BadAuth("Invalid authorization header", status_code=status.HTTP_401_UNAUTHORIZED)

    token_raw = authorization.replace("Bearer ", "")
    if len(token_raw) != 43:
        raise BadAuth("Invalid token format", status_code=status.HTTP_401_UNAUTHORIZED)

    reader = AccessTokenReader(session)
    token_hash = hash_token(token_raw)
    token_brief = await reader.get(token_hash)

    if token_brief is None:
        raise BadAuth("Invalid access token", status_code=status.HTTP_401_UNAUTHORIZED)

    return token_brief


def get_mediator(request: Request) -> Mediator:
    return request.app.state.mediator

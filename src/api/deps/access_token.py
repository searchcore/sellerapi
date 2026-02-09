import hashlib

from fastapi import Header, status
from dishka.integrations.fastapi import (
    FromDishka,
    inject,
)

from src.api.exceptions import BadAuth

from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.dtos import AccessTokenBriefDTO

from src.infrastructure.adapters.access_token_reader import AccessTokenReader


def hash_token(access_token_raw: str) -> str:
    return hashlib.sha256(access_token_raw.encode()).hexdigest()


@inject
async def get_access_token(
    session: FromDishka[AsyncSession],
    authorization: str = Header(...)
) -> AccessTokenBriefDTO:
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

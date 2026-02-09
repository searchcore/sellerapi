from dataclasses import dataclass


@dataclass(frozen=True)
class AccessTokenBriefDTO:
    id: int
    token_hash: str

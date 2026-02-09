from dataclasses import dataclass


@dataclass(frozen=True)
class CreatedTokenDTO:
    token_id: int
    token: str

from dataclasses import dataclass


@dataclass(frozen=True)
class FeatureDTO:
    id: int
    code: str

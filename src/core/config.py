from dataclasses import dataclass

from .loader import load_config


@dataclass(frozen=True)
class Config:
    PROJECT_NAME: str = "Seller API"
    API_V1_PREFIX: str = "/api/v1"

    DEBUG: bool = False


@dataclass(frozen=True)
class DatabaseConfig:
    dsn: str


config = load_config(Config, "app")

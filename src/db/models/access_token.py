from datetime import datetime

from sqlalchemy import (
    Integer, DateTime, String
)
from sqlalchemy.orm import Mapped, mapped_column

from .base import TimedBaseModel


class AccessTokenModel(TimedBaseModel):
    __tablename__ = "access_tokens"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    token_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

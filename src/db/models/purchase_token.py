from datetime import datetime

from sqlalchemy import (
    Integer, DateTime, String, BOOLEAN, ForeignKey
)
from sqlalchemy.orm import Mapped, mapped_column

from .base import TimedBaseModel


class PurchaseTokenModel(TimedBaseModel):
    __tablename__ = "purchase_tokens"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_type: Mapped[int] = mapped_column(ForeignKey("product_types.id"), nullable=False)
    token_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    available_to_buy: Mapped[int] = mapped_column(Integer, nullable=False)
    used_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(BOOLEAN, default=True, nullable=False)

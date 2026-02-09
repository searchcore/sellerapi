from datetime import datetime

from sqlalchemy import (
    Integer, DateTime, ForeignKey
)
from sqlalchemy.orm import Mapped, mapped_column

from .base import TimedBaseModel


class ProductPurchaseModel(TimedBaseModel):
    __tablename__ = "product_purchases"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False, index=True, unique=True)
    token_id: Mapped[int] = mapped_column(ForeignKey("purchase_tokens.id"), nullable=False)
    bought_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

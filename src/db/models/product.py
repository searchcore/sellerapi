from datetime import datetime

from sqlalchemy import (
    Integer, BOOLEAN, DateTime, ForeignKey
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

from .base import TimedBaseModel


class ProductModel(TimedBaseModel):
    __tablename__ = "products"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[int] = mapped_column(ForeignKey("product_types.id"), nullable=False)
    schema: Mapped[int] = mapped_column(ForeignKey("product_schema_versions.id"), nullable=False)
    content: Mapped[dict] = mapped_column(JSONB, nullable=False)
    valid: Mapped[bool] = mapped_column(BOOLEAN, default=True, nullable=False)
    reserved_until: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

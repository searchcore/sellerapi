from sqlalchemy import (
    Integer, ForeignKey, UniqueConstraint, CheckConstraint
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

from .base import TimedBaseModel


class ProductSchemaVersionModel(TimedBaseModel):
    __tablename__ = "product_schema_versions"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_type: Mapped[int] = mapped_column(ForeignKey("product_types.id"), nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    schema: Mapped[dict] = mapped_column(JSONB, nullable=False)

    __table_args__ = (
        UniqueConstraint("product_type", "version"),
        CheckConstraint("version > 0", name="version_gt_than_zero")
    )

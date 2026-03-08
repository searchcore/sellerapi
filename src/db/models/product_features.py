from sqlalchemy import (
    ForeignKey
)
from sqlalchemy.orm import Mapped, mapped_column

from .base import TimedBaseModel


class ProductFeaturesModel(TimedBaseModel):
    __tablename__ = "product_features"
    __mapper_args__ = {"eager_defaults": True}

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False, primary_key=True)
    feature_id: Mapped[int] = mapped_column(ForeignKey("product_features_catalog.id"), nullable=False, primary_key=True)

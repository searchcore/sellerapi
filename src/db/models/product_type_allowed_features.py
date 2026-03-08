from sqlalchemy import (
    ForeignKey
)
from sqlalchemy.orm import Mapped, mapped_column

from .base import TimedBaseModel


class ProductTypeAllowedFeaturesModel(TimedBaseModel):
    __tablename__ = "product_type_features"
    __mapper_args__ = {"eager_defaults": True}

    product_type: Mapped[int] = mapped_column(ForeignKey("product_types.id"), nullable=False, primary_key=True)
    feature: Mapped[int] = mapped_column(ForeignKey("product_features_catalog.id"), nullable=False, primary_key=True)

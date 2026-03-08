from sqlalchemy import (
    Integer, String
)
from sqlalchemy.orm import Mapped, mapped_column

from .base import TimedBaseModel


class ProductTypeFeaturesModel(TimedBaseModel):
    __tablename__ = "product_features_catalog"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(100), nullable=True)

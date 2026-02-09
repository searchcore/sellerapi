from sqlalchemy import (
    Integer, String
)
from sqlalchemy.orm import Mapped, mapped_column

from .base import TimedBaseModel


class ProductTypeModel(TimedBaseModel):
    __tablename__ = "product_types"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

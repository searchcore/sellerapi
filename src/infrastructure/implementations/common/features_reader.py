from src.application.common.interfaces import IFeaturesReader

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import ProductTypeFeaturesModel, ProductTypeAllowedFeaturesModel

from src.domain.common.value_objects import ProductTypeIDVO

from src.application.common.dtos import FeatureDTO


class FeaturesReader(IFeaturesReader):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_allowed_features_codes(self, product_type: ProductTypeIDVO) -> list[str]:
        stmt = (
            select(ProductTypeFeaturesModel.code)
            .join(ProductTypeAllowedFeaturesModel, ProductTypeAllowedFeaturesModel.feature == ProductTypeFeaturesModel.id)
            .where(
                ProductTypeAllowedFeaturesModel.product_type == product_type.value,
            )
        )

        result = await self._session.execute(stmt)

        return result.scalars().all()

    async def get_features_by_code(self, feature_codes: list[str]) -> list[FeatureDTO]:
        stmt = (
            select(ProductTypeFeaturesModel.code, ProductTypeFeaturesModel.id)
            .where(
                ProductTypeFeaturesModel.code.in_(feature_codes)
            )
        )

        result = await self._session.execute(stmt)

        return [FeatureDTO(row.id, row.code) for row in result.all()]

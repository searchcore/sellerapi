from abc import ABC, abstractmethod

from src.domain.common.value_objects import ProductTypeIDVO

from src.application.common.dtos import FeatureDTO


class IFeaturesReader(ABC):
    @abstractmethod
    async def get_allowed_features_codes(self, product_type: ProductTypeIDVO) -> list[str]:
        ...

    @abstractmethod
    async def get_features_by_code(self, feature_codes: list[str]) -> list[FeatureDTO]:
        ...

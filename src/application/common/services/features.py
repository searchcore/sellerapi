from operator import attrgetter

from src.domain.common.value_objects import ProductTypeIDVO

from src.application.common.dtos import FeatureDTO

from src.application.common.exceptions import ProductTypeFeatureInvalid

from src.application.common.interfaces import IFeaturesReader


class FeaturesService:
    def __init__(
        self,
        features_reader: IFeaturesReader, 
    ):
        self._features_reader = features_reader

    async def get_features_by_codes(self, product_type: ProductTypeIDVO, codes: list[str]) -> list[FeatureDTO]:
        features = await self._features_reader.get_features_by_code(codes)
        if len(features) != len(codes):
            existing_features_codes = [f.code for f in features]
            not_existing_features = list(set(codes).difference(existing_features_codes))

            raise ProductTypeFeatureInvalid(
                f"Provided features ({'\''.join(not_existing_features)}) not found.",
                params={
                    "invalid_features": not_existing_features
                }
            )

        allowed_features = await self._features_reader.get_allowed_features_codes(product_type)
        not_allowed_features = list(set(codes).difference(allowed_features))
        if not_allowed_features:
            raise ProductTypeFeatureInvalid(
                f"Provided features ({'\''.join(not_allowed_features)}) can't be used with product of type {product_type.value}",
                params={
                    "invalid_features": not_allowed_features,
                }
            )

        return features

    async def get_ids_by_codes(self, product_type: ProductTypeIDVO, codes: list[str]) -> list[int]:
        features = await self.get_features_by_codes(product_type, codes)
        return list(map(attrgetter("id"), features))

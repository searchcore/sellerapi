from abc import ABC, abstractmethod

from src.domain.common.value_objects import ProductTypeIDVO


class IProductsReader(ABC):
    @abstractmethod
    async def does_product_type_exist(self, id: ProductTypeIDVO) -> bool:
        ...

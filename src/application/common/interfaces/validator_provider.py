from abc import ABC, abstractmethod

from src.application.common.content_validators import BaseValidator


class IValidatorProvider(ABC):
    @abstractmethod
    def get_validator(self, product_id: int) -> BaseValidator:
        ...

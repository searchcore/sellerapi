from src.application.common.interfaces import IValidatorProvider

from src.application.common.content_validators import BaseValidator

from src.application.common.content_validators.default_validator import DefaultValidator


class FakeValidatorProvider(IValidatorProvider):
    def get_validator(self, product_id: int) -> BaseValidator:
        return DefaultValidator()

from src.application.common.interfaces import IValidatorProvider
from src.application.common.content_validators.abc import BaseValidator

from src.infrastructure.validators_registry import ValidatorRegistry


class ValidatorProvider(IValidatorProvider):
    def __init__(self, validator_registry: ValidatorRegistry):
        self._validator_registry = validator_registry

    def get_validator(self, product_id: int) -> BaseValidator:
        return self._validator_registry.get_validator(product_id)

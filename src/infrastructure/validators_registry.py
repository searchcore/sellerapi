import importlib
import inspect
import pkgutil
from pathlib import Path
from typing import Type
from src.application.common.content_validators.abc import BaseValidator


class ValidatorRegistry:
    def __init__(self, default_validator: Type[BaseValidator]):
        self._validators: dict[int, Type[BaseValidator]] = {}
        self._default_validator = default_validator

    def register_validators(self, package: str = "src.validators"):
        package_obj = importlib.import_module(package)
        package_path = Path(package_obj.__file__).parent

        for finder, module_name, is_pkg in pkgutil.iter_modules([str(package_path)]):
            full_module_name = f"{package}.{module_name}"
            module = importlib.import_module(full_module_name)
            for _, cls in inspect.getmembers(module, inspect.isclass):
                if issubclass(cls, BaseValidator) and cls is not BaseValidator:
                    if not hasattr(cls, "__product_id__"):
                        raise ValueError(f"Validator {cls.__name__} must have '__product_id__' attribute")
                    validator_product_id: int = getattr(cls, "__product_id__")

                    self._validators[validator_product_id] = cls

    def get_validator(self, product_id: int) -> BaseValidator:
        validator_cls = self._validators.get(product_id)
        if not validator_cls:
            return self._default_validator()
        return validator_cls()

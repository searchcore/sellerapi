from abc import ABC, abstractmethod

from dataclasses import dataclass, field
from typing import Any

from src.domain.common.value_objects import ProductTypeSchemaVO


@dataclass(frozen=True)
class ContentInvalidReason:
    details: str
    params: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ValidationExecutionError:
    details: str
    params: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ContentValidationReport:
    violations: list[ContentInvalidReason]
    execution_error: ValidationExecutionError | None = None

    @property
    def product_valid(self) -> bool:
        return not self.violations and not self.execution_error


class ISchemaValidator(ABC):
    @abstractmethod
    def is_schema_valid(self, schema: ProductTypeSchemaVO) -> bool:
        ...

    @abstractmethod
    def validate_content(self, content: dict[str, Any], schema: ProductTypeSchemaVO) -> ContentValidationReport:
        ...

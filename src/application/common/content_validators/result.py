from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ProductInvalidReason:
    details: str
    params: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ValidationExecutionError:
    details: str
    params: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ProductValidationReport:
    product_id: int
    violations: list[ProductInvalidReason]
    execution_error: ValidationExecutionError | None = None

    @property
    def product_valid(self) -> bool:
        return not self.violations and not self.execution_error

import asyncio
from typing import Any, ClassVar
from dataclasses import dataclass
from abc import ABC, abstractmethod
import logging

from .result import ProductInvalidReason, ValidationExecutionError, ProductValidationReport


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class IdentifiedProduct:
    id: int
    content: dict[str, Any]


class BaseValidator(ABC):
    __product_id__: ClassVar[int] = None


    @abstractmethod
    async def validate(self, content: dict[str, Any]) -> list[ProductInvalidReason]:
        ...


    async def batch_validate(self, products: list[IdentifiedProduct], concurrency: int = 10) -> list[ProductValidationReport]:
        semaphore = asyncio.Semaphore(concurrency)

        async def validate_one(product: IdentifiedProduct):
            async with semaphore:
                execution_error: ValidationExecutionError | None = None
                violations: list[ProductInvalidReason] = []
                try:
                    violations = await self.validate(product.content)
                except Exception as e:
                    logger.exception(
                        "unknown_validation_exception",
                    )
                    execution_error = ValidationExecutionError("Unexpected error during validation process!")
                return ProductValidationReport(product.id, violations, execution_error)

        results = await asyncio.gather(*(validate_one(p) for p in products))

        return results

from src.application.common.interfaces.schema_validator import ISchemaValidator, ContentValidationReport, ContentInvalidReason, ValidationExecutionError
from src.domain.common.value_objects import ProductTypeSchemaVO

from logging import getLogger

from typing import Any

from jsonschema import validate, ValidationError
from jsonschema.validators import validator_for


logger = getLogger(__name__)


class SchemaValidator(ISchemaValidator):
    def is_schema_valid(self, schema: ProductTypeSchemaVO) -> bool:
        validator = validator_for(schema.value)

        try:
            validator.check_schema(schema.value)
        except Exception as e:
            logger.info("Schema is invalid", exc_info=True)
            return False
        
        return True

    def validate_content(self, content: dict[str, Any], schema: ProductTypeSchemaVO) -> ContentValidationReport:
        violations: list[ContentInvalidReason] = []
        execution_error: ValidationExecutionError | None = None
        try:
            validate(content, schema.value)
        except ValidationError as e:
            violations.append(ContentInvalidReason(details=e.message))
        except Exception as e:
            logger.warning("Unexpected exception validating content schema!", exc_info=True)
            execution_error = ValidationExecutionError(details="Unexpected error validating content schema!")

        return ContentValidationReport(violations, execution_error)

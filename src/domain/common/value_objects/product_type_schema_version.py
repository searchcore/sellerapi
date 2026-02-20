from dataclasses import dataclass


@dataclass(frozen=True)
class ProductTypeSchemaVersionVO:
    value: int

from typing import Any

from src.application.common.content_validators import BaseValidator, ProductInvalidReason


class DefaultValidator(BaseValidator):
    async def validate(self, content: dict[Any, None]) -> list[ProductInvalidReason]:
        if not len(content.keys()):
            return [ProductInvalidReason("Empty product provided")]
    
        for k, v in content.items():
            if v:
                return []
        
        return [ProductInvalidReason("Provided product does not contain any value")]

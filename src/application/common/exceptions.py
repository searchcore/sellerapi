from src.core.exceptions import BaseAppException, ErrorCodes


class ApplicationLayerException(BaseAppException):
    code = ErrorCodes.UNEXPECTED


class PurchaseTokenNotFound(ApplicationLayerException):
    code = ErrorCodes.PURCHASE_TOKEN_NOT_FOUND


class ProductOutOfStock(ApplicationLayerException):
    code = ErrorCodes.PRODUCT_OUT_OF_STOCK


class ProductTypeSchemaInvalid(ApplicationLayerException):
    code = ErrorCodes.PRODUCT_TYPE_SCHEMA_INVALID

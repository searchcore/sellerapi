from fastapi import APIRouter

from src.api.v1.admin.router import router as admin_router
from src.api.v1.customer.router import router as customer_router

from src.core.config import config


router = APIRouter()
router.include_router(admin_router, prefix="/admin", tags=["admin"], include_in_schema=config.ADMIN_DOCS)
router.include_router(customer_router, prefix="/customer", tags=["customer"])

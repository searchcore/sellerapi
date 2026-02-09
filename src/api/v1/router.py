from fastapi import APIRouter

from src.api.v1.admin.router import router as admin_router
from src.api.v1.customer.router import router as customer_router

router = APIRouter()
router.include_router(admin_router, prefix="/admin", tags=["admin"])
router.include_router(customer_router, prefix="/customer", tags=["customer"])

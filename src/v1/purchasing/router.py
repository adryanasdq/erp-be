from fastapi import APIRouter

from src.v1.purchasing.supplier.router import router as supplier_router


purchasing_router = APIRouter(prefix="/purchasing")

purchasing_router.include_router(supplier_router)
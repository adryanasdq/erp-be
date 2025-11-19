from fastapi import APIRouter

from src.v1.inventory.warehouse.router import router as warehouse_router


inventory_router = APIRouter(prefix="/warehouse")

inventory_router.include_router(warehouse_router)
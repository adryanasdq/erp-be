from fastapi import APIRouter

from src.v1.inventory.warehouse.router import router as warehouse_router
from src.v1.inventory.unit_of_measure.router import router as uom_router
from src.v1.inventory.item.router import router as item_router


inventory_router = APIRouter(prefix="/inventory")

inventory_router.include_router(warehouse_router)
inventory_router.include_router(uom_router)
inventory_router.include_router(item_router)
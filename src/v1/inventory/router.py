from fastapi import APIRouter

from src.v1.inventory.warehouse.router import router as warehouse_router
from src.v1.inventory.unit_of_measure.router import router as uom_router
from src.v1.inventory.item.router import router as item_router
from src.v1.inventory.stock_balance.router import router as stock_balance_router
from src.v1.inventory.stock_movement.router import router as stock_movement_router


inventory_router = APIRouter(prefix="/inventory")

inventory_router.include_router(warehouse_router)
inventory_router.include_router(uom_router)
inventory_router.include_router(item_router)
inventory_router.include_router(stock_balance_router)
inventory_router.include_router(stock_movement_router)
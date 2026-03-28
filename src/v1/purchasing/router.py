from fastapi import APIRouter

from src.v1.purchasing.supplier.router import router as supplier_router
from src.v1.purchasing.purchase_order.router import router as purchase_order_router
from src.v1.purchasing.good_receipt.router import router as goods_receipt_router


purchasing_router = APIRouter(prefix="/purchasing")

purchasing_router.include_router(supplier_router)
purchasing_router.include_router(purchase_order_router)
purchasing_router.include_router(goods_receipt_router)

from fastapi import APIRouter

from src.v1.sales.customer.router import router as customer_router
from src.v1.sales.delivery.router import router as delivery_router
from src.v1.sales.sales_order.router import router as sales_order_router


sales_router = APIRouter(prefix="/sales")

sales_router.include_router(customer_router)
sales_router.include_router(delivery_router)
sales_router.include_router(sales_order_router)

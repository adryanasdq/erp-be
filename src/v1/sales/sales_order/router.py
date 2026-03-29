from fastapi import APIRouter, Depends
from sqlmodel import Session as SessionType
from src.core.settings.database import get_session
from src.core.schemas.sales.sales_order import SalesOrderSchema
from .dependency import validate_so, get_so_by_id
from .service import create, confirm_so # confirm_so is the reservation logic we wrote

router = APIRouter(prefix="/sales-orders", tags=["Sales Orders"])

@router.post("/")
def create_sales_order(data: SalesOrderSchema, session: SessionType = Depends(get_session)):
    validated = validate_so(data, session)
    return create(validated, session)

@router.post("/{id}/confirm")
def confirm_sales_order(id: str, session: SessionType = Depends(get_session)):
    # This triggers the reservation logic in StockBalance
    return confirm_so(id, session)
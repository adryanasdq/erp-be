from fastapi import APIRouter, Depends
from sqlmodel import Session as SessionType
from src.core.settings.database import get_session
from src.core.schemas.sales.sales_order import SalesOrderSchema
from .dependency import validate_so_creation, validate_so_confirmation
from .service import commit_so_transaction

router = APIRouter(prefix="/sales-orders", tags=["Sales Orders"])

@router.post("/")
def create_sales_order(data: SalesOrderSchema, session: SessionType = Depends(get_session)):
    # 1. Process/Validate
    db_so = validate_so_creation(data, session)
    # 2. Commit
    return commit_so_transaction(db_so, session)

@router.post("/{id}/confirm")
def confirm_sales_order(id: str, session: SessionType = Depends(get_session)):
    # 1. Logic Processing (Reservation)
    db_so = validate_so_confirmation(id, session)
    # 2. Commit
    return commit_so_transaction(db_so, session)

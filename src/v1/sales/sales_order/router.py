from fastapi import APIRouter, Depends
from sqlmodel import Session as SessionType
from src.core.settings.database import get_session
from src.core.schemas.sales.sales_order import SalesOrderSchema
from .dependency import (
    validate_so_creation,
    validate_so_confirmation,
    validate_so_update,
    validate_so_cancellation,
    get_so_by_id,
)
from .service import commit_so_transaction, get_all

router = APIRouter(prefix="/sales-orders", tags=["Sales Orders"])


@router.post("/")
def create_sales_order(
    data: SalesOrderSchema, session: SessionType = Depends(get_session)
):
    db_so = validate_so_creation(data, session)

    return commit_so_transaction(db_so, session)


@router.post("/{id}/confirm")
def confirm_sales_order(id: str, session: SessionType = Depends(get_session)):
    db_so = validate_so_confirmation(id, session)

    return commit_so_transaction(db_so, session)


@router.get("/")
def list_sales_orders(session: SessionType = Depends(get_session)):
    return get_all(session)


@router.get("/{id}")
def get_sales_order_detail(id: str, session: SessionType = Depends(get_session)):
    return get_so_by_id(id, session)


@router.patch("/{id}")
def update_sales_order(
    id: str, data: SalesOrderSchema, session: SessionType = Depends(get_session)
):
    db_so = validate_so_update(id, data, session)
    return commit_so_transaction(db_so, session)


@router.post("/{id}/cancel")
def cancel_sales_order(id: str, session: SessionType = Depends(get_session)):
    # Reverses reservations and kills the order
    db_so = validate_so_cancellation(id, session)
    return commit_so_transaction(db_so, session)

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session as SessionType
from src.core.settings.database import get_session
from src.core.schemas.sales.delivery import DeliverySchema

from .dependency import (
    validate_delivery_processing,
    get_delivery_by_id,
    get_all_deliveries,
)
from .service import commit_delivery_transaction

router = APIRouter(prefix="/deliveries", tags=["Deliveries"])


@router.get("/")
def list_deliveries(
    so_id: str = Query(None, description="Filter by Sales Order ID"),
    session: SessionType = Depends(get_session),
):
    """List all deliveries, optionally filtered by a specific SO."""
    return get_all_deliveries(session, so_id)


@router.get("/{id}")
def get_delivery_detail(id: str, session: SessionType = Depends(get_session)):
    """Fetch the full details of a specific delivery note."""
    return get_delivery_by_id(id, session)


@router.post("/")
def create_delivery(data: DeliverySchema, session: SessionType = Depends(get_session)):
    processed_data = validate_delivery_processing(data, session)

    return commit_delivery_transaction(processed_data, session)

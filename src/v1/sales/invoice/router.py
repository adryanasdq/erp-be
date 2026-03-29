from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session as SessionType
from src.core.schemas.sales.invoice import InvoiceSchema
from src.core.settings.database import get_session
from .dependency import validate_invoice_processing, get_invoice_by_id, get_all_invoices
from .service import commit_invoice_transaction

router = APIRouter(prefix="/sales/invoices", tags=["Invoices"])


@router.post("/")
def create_invoice(data: InvoiceSchema, session: SessionType = Depends(get_session)):
    processed_data = validate_invoice_processing(data, session)

    return commit_invoice_transaction(processed_data, session)


@router.get("/{id}")
def get_invoice(id: str, session: SessionType = Depends(get_session)):

    return get_invoice_by_id(id, session)


@router.get("/")
def list_invoices(
    customer_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    session: SessionType = Depends(get_session),
):
    """Dashboard view for all invoices/AR."""
    return get_all_invoices(session, customer_id, status)

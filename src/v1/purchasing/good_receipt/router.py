from fastapi import APIRouter, Depends, Query
from sqlmodel import Session as SessionType
from src.core.settings.database import get_session
from src.core.schemas.purchasing.goods_receipt import GoodsReceiptSchema
from .dependency import (
    get_all_grns,
    get_grn_by_id,
    validate_grn_cancellation,
    validate_grn_processing,
)
from .service import commit_grn_cancellation, commit_grn_transaction

router = APIRouter(prefix="/goods-receipts", tags=["Goods Receipt (GRN)"])


@router.get("/")
def list_goods_receipts(
    po_id: str = Query(None, description="Filter by Purchase Order ID"),
    session: SessionType = Depends(get_session),
):
    return get_all_grns(session, po_id)


@router.get("/{id}")
def get_grn_detail(id: str, session: SessionType = Depends(get_session)):
    return get_grn_by_id(id, session)


@router.post("/{id}/cancel")
def cancel_goods_receipt(id: str, session: SessionType = Depends(get_session)):
    db_grn, inventory_pairs = validate_grn_cancellation(id, session)

    return commit_grn_cancellation(db_grn, inventory_pairs, session)


@router.post("/")
def create_grn(data: GoodsReceiptSchema, session: SessionType = Depends(get_session)):
    processed_data = validate_grn_processing(data, session)

    return commit_grn_transaction(processed_data, session)

from fastapi import APIRouter, Depends
from sqlmodel import Session as SessionType

from src.core.schemas.purchasing.goods_receipt import GoodsReceiptSchema
from src.core.settings.database import get_session

from .dependency import validate_grn
from .service import create, get_all, get_by_id
from .exception import GRNNotFound


router = APIRouter(prefix="/goods-receipts", tags=["Goods Receipts"])


@router.post("/")
def create_goods_receipt(
    data: GoodsReceiptSchema, 
    session: SessionType = Depends(get_session)
):
    # Dependency handles checking PO, Warehouse, and mapping lines
    validated_grn = validate_grn(data, session)
    return create(validated_grn, session)


@router.get("/")
def get_all_grns(session: SessionType = Depends(get_session)):
    return get_all(session)


@router.get("/{id}")
def get_grn(id: str, session: SessionType = Depends(get_session)):
    grn = get_by_id(id, session)
    if not grn:
        raise GRNNotFound()
    return grn
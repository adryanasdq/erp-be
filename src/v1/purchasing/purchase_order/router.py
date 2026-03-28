from fastapi import APIRouter, Depends
from sqlmodel import Session as SessionType

from src.core.schemas.purchasing.purchase_order import PurchaseOrderSchema
from src.core.settings.database import get_session

from .dependency import get_po_by_id, validate_po
from .service import get_all, get_by_id, create, update, delete


router = APIRouter(prefix="/purchase-orders", tags=["Purchase Orders"])


@router.get("/")
def get_all_pos(session=Depends(get_session)):
    return get_all(session)


@router.get("/{id}")
def get_po(id: str, session=Depends(get_session)):
    return get_by_id(id, session)


@router.post("/")
def create_po(data: PurchaseOrderSchema, session: SessionType = Depends(get_session)):
    validated_po = validate_po(data, session)
    return create(validated_po, session)


@router.put("/{id}")
def update_po(id: str, data: PurchaseOrderSchema, session: SessionType = Depends(get_session)):
    validated_po = validate_po(data, session, id)
    return update(validated_po, session)


@router.delete("/{id}")
def delete_po(data=Depends(get_po_by_id), session: SessionType = Depends(get_session)):
    return delete(data, session)
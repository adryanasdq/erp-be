from fastapi import APIRouter, Depends
from sqlmodel import Session as SessionType

from src.core.schemas.purchasing.supplier import Supplier
from src.core.settings.database import get_session

from .dependency import get_supplier_by_id, validate_supplier
from .service import get_all, get_by_id, create, update, delete


router = APIRouter(prefix="/suppliers", tags=["Suppliers"])


@router.get("/")
def get_all_suppliers(session=Depends(get_session)):
    suppliers = get_all(session)
    return suppliers


@router.get("/{id}")
def get_supplier(id: str, session=Depends(get_session)):
    supplier = get_by_id(id, session)
    return supplier


@router.post("/")
def create_supplier(data: Supplier, session: SessionType = Depends(get_session)):
    validated_supplier = validate_supplier(data, session)
    return create(validated_supplier, session)


@router.put("/{id}")
def update_supplier(
    id: str, data: Supplier, session: SessionType = Depends(get_session)
):
    validated_supplier = validate_supplier(data, session, id)
    return update(validated_supplier, session)


@router.delete("/{id}")
def delete_supplier(
    data: Supplier = Depends(get_supplier_by_id),
    session: SessionType = Depends(get_session),
):
    return delete(data, session)
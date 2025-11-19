from fastapi import APIRouter, Depends
from sqlmodel import Session as SessionType

from src.core.schemas.inventory.warehouse import Warehouse
from src.core.settings.database import get_session

from .dependency import get_warehouse_by_id, validate_warehouse
from .service import get_all, get_by_id, create, update, delete


router = APIRouter(prefix="/warehouses", tags=["Warehouses"])


@router.get("/")
def get_all_warehouses(session = Depends(get_session)):
    warehouses = get_all(session)
    return warehouses


@router.get("/{id}")
def get_warehouse(id: str, session = Depends(get_session)):
    warehouse = get_by_id(id, session)
    return warehouse


@router.post("/")
def create_warehouse(data: Warehouse, session: SessionType = Depends(get_session)):
    validated_warehouse = validate_warehouse(data, session)
    return create(validated_warehouse, session)


@router.put("/{id}")
def update_warehouse(
    id: str, data: Warehouse, session: SessionType = Depends(get_session)
):
    validated_warehouse = validate_warehouse(data, session, id)
    return update(validated_warehouse, session)


@router.delete("/{id}")
def delete_warehouse(
    data: Warehouse = Depends(get_warehouse_by_id),
    session: SessionType = Depends(get_session),
):
    return delete(data, session)
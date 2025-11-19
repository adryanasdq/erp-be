from fastapi import APIRouter, Depends
from sqlmodel import Session as SessionType

from src.core.schemas.inventory.uom import UnitOfMeasure
from src.core.settings.database import get_session

from .dependency import get_uom_by_id, validate_uom
from .service import get_all, get_by_id, create, update, delete


router = APIRouter(prefix="/uom", tags=["Unit Of Measure"])


@router.get("/")
def get_all_uoms(session=Depends(get_session)):
    uoms = get_all(session)
    return uoms


@router.get("/{id}")
def get_uom(id: str, session=Depends(get_session)):
    uom = get_by_id(id, session)
    return uom


@router.post("/")
def create_uom(data: UnitOfMeasure, session: SessionType = Depends(get_session)):
    validated_uom = validate_uom(data, session)
    return create(validated_uom, session)


@router.put("/{id}")
def update_uom(
    id: str, data: UnitOfMeasure, session: SessionType = Depends(get_session)
):
    validated_uom = validate_uom(data, session, id)
    return update(validated_uom, session)


@router.delete("/{id}")
def delete_uom(
    data: UnitOfMeasure = Depends(get_uom_by_id),
    session: SessionType = Depends(get_session),
):
    return delete(data, session)

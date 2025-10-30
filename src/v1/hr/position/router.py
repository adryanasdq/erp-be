from fastapi import APIRouter, Depends
from sqlmodel import Session as SessionType

from src.core.schemas.hr.position import Position
from src.core.settings.database import get_session

from .dependency import get_position_by_id, validate_position
from .service import get_all, get_by_id, create, update, delete


router = APIRouter(prefix="/positions", tags=["Positions"])


@router.get("/")
def get_all_positions(session = Depends(get_session)):
    positions = get_all(session)
    return positions


@router.get("/{id}")
def get_position(id: str, session = Depends(get_session)):
    position = get_by_id(id, session)
    return position


@router.post("/")
def create_position(data: Position, session: SessionType = Depends(get_session)):
    validated_position = validate_position(data, session)
    return create(validated_position, session)


@router.put("/{id}")
def update_position(
    id: str, data: Position, session: SessionType = Depends(get_session)
):
    validated_position = validate_position(data, session, id)
    return update(validated_position, session)


@router.delete("/{id}")
def delete_position(
    data: Position = Depends(get_position_by_id),
    session: SessionType = Depends(get_session),
):
    return delete(data, session)

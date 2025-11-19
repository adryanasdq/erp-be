from fastapi import APIRouter, Depends
from sqlmodel import Session as SessionType

from src.core.schemas.inventory.item import Item
from src.core.settings.database import get_session

from .dependency import get_item_by_id, validate_item
from .service import get_all, get_by_id, create, update, delete


router = APIRouter(prefix="/items", tags=["Items"])


@router.get("/")
def get_all_items(session=Depends(get_session)):
    items = get_all(session)
    return items


@router.get("/{id}")
def get_item(id: str, session=Depends(get_session)):
    item = get_by_id(id, session)
    return item


@router.post("/")
def create_item(data: Item, session: SessionType = Depends(get_session)):
    validated_item = validate_item(data, session)
    return create(validated_item, session)


@router.put("/{id}")
def update_item(
    id: str, data: Item, session: SessionType = Depends(get_session)
):
    validated_item = validate_item(data, session, id)
    return update(validated_item, session)


@router.delete("/{id}")
def delete_item(
    data: Item = Depends(get_item_by_id),
    session: SessionType = Depends(get_session),
):
    return delete(data, session)

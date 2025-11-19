from datetime import datetime
from fastapi import Depends
from sqlmodel import Session as SessionType

from src.core.settings.database import get_session
from src.core.models.inventory.item import Item as DbItem
from src.core.schemas.inventory.item import Item

from .exception import ItemIdExists, ItemNotFound
from ..unit_of_measure.dependency import get_uom_by_id


def check_if_item_exists(item_id: str, session: SessionType):
    db_item = session.get(DbItem, item_id)
    if db_item:
        raise ItemIdExists()
    return


def get_item_by_id(
    id: str, session: SessionType = Depends(get_session)
):
    db_item = session.get(DbItem, id)
    if not db_item:
        raise ItemNotFound()
    return db_item


def validate_item(item: Item, session: SessionType, id: str = None):
    get_uom_by_id(item.uom_id, session)

    if not id:
        db_item = DbItem(
            **item.model_dump(exclude_unset=True, exclude={"id"})
        )
    else:
        db_item = get_item_by_id(id, session)
        for key, attr in item.model_dump(exclude_unset=True).items():
            setattr(db_item, key, attr)

    db_item.modified_date = datetime.now()
    return db_item
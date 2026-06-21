from datetime import datetime
from fastapi import Depends
from sqlmodel import Session as SessionType, select

from src.core.settings.database import get_session
from src.core.models.inventory.item import Item as DbItem
from src.core.schemas.inventory.item import Item

from .exception import ItemNotFound, ItemSKUExists
from ..unit_of_measure.dependency import get_uom_by_id


def check_if_item_exists(item: Item, session: SessionType):    
    statement = select(DbItem).where(DbItem.sku == item.sku)
    db_item_sku = session.exec(statement).first()
    if db_item_sku:
        raise ItemSKUExists(item.sku)
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
        check_if_item_exists(item, session)
        
        db_item = DbItem(
            **item.model_dump(exclude_unset=True, exclude={"id"})
        )
    else:
        db_item = get_item_by_id(id, session)
        for key, attr in item.model_dump(exclude_unset=True).items():
            setattr(db_item, key, attr)

    db_item.modified_date = datetime.now()
    return db_item
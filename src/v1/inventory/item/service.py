from fastapi import HTTPException
from sqlmodel import select, Session as SessionType

from src.core.models.inventory.item import Item as DbItem
from src.core.schemas.inventory.item import Item


def get_all(session: SessionType):
    stmnt = select(DbItem)

    result = session.exec(stmnt)
    return result.all()


def get_by_id(item_id: str, session: SessionType):
    stmnt = select(DbItem).where(DbItem.id == item_id)

    result = session.exec(stmnt)
    return result.first()


def create(item: DbItem, session: SessionType):
    try:
        session.add(item)
        session.commit()
        session.refresh(item)
        return Item.model_validate(item)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def update(item: DbItem, session: SessionType):
    try:
        session.commit()
        session.refresh(item)
        return Item.model_validate(item)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    

def delete(item: DbItem, session: SessionType):
    try:
        session.delete(item)
        session.commit()
        return {"message": f"Item with id {item.id} deleted successfully"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
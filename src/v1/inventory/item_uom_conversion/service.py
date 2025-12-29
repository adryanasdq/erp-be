from fastapi import HTTPException
from sqlmodel import select, Session as SessionType

from src.core.models.inventory.item_uom_conversion import ItemUOMConversion as DbItemUOMConversion
from src.core.schemas.inventory.item_uom_conversion import ItemUOMConversion


def get_all(session: SessionType):
    stmnt = select(DbItemUOMConversion)

    result = session.exec(stmnt)
    return result.all()


def get_by_id(conv_id: str, session: SessionType):
    stmnt = select(DbItemUOMConversion).where(DbItemUOMConversion.id == conv_id)

    result = session.exec(stmnt)
    return result.first()


def create(conv: DbItemUOMConversion, session: SessionType):
    try:
        session.add(conv)
        session.commit()
        session.refresh(conv)
        return ItemUOMConversion.model_validate(conv)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    

def unactive(conv: DbItemUOMConversion, session: SessionType):
    try:
        conv.is_active = False
        session.commit()
        return {"message": f"Conversion with id {conv.id} deleted successfully"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
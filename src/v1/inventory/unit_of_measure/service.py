from fastapi import HTTPException
from sqlmodel import select, Session as SessionType

from src.core.models.inventory.uom import UnitOfMeasure as DbUnitOfMeasure
from src.core.schemas.inventory.uom import UnitOfMeasure


def get_all(session: SessionType):
    stmnt = select(DbUnitOfMeasure)

    result = session.exec(stmnt)
    return result.all()


def get_by_id(uom_id: str, session: SessionType):
    stmnt = select(DbUnitOfMeasure).where(DbUnitOfMeasure.id == uom_id)

    result = session.exec(stmnt)
    return result.first()


def create(uom: DbUnitOfMeasure, session: SessionType):
    try:
        session.add(uom)
        session.commit()
        session.refresh(uom)
        return UnitOfMeasure.model_validate(uom)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def update(uom: DbUnitOfMeasure, session: SessionType):
    try:
        session.commit()
        session.refresh(uom)
        return UnitOfMeasure.model_validate(uom)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    

def delete(uom: DbUnitOfMeasure, session: SessionType):
    try:
        session.delete(uom)
        session.commit()
        return {"message": f"Unit of measure with id {uom.id} deleted successfully"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
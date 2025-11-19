from fastapi import HTTPException
from sqlmodel import select, Session as SessionType

from src.core.models.inventory.warehouse import Warehouse as DbWarehouse
from src.core.schemas.inventory.warehouse import Warehouse


def get_all(session: SessionType):
    stmnt = select(DbWarehouse)

    result = session.exec(stmnt)
    return result.all()


def get_by_id(warehouse_id: str, session: SessionType):
    stmnt = select(DbWarehouse).where(DbWarehouse.id == warehouse_id)

    result = session.exec(stmnt)
    return result.first()


def create(position: DbWarehouse, session: SessionType):
    try:
        session.add(position)
        session.commit()
        session.refresh(position)
        return Warehouse.model_validate(position)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def update(position: DbWarehouse, session: SessionType):
    try:
        session.commit()
        session.refresh(position)
        return Warehouse.model_validate(position)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    

def delete(position: DbWarehouse, session: SessionType):
    try:
        session.delete(position)
        session.commit()
        return {"message": f"Position with id {position.id} deleted successfully"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
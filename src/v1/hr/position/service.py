from fastapi import HTTPException
from sqlmodel import select
from sqlmodel import Session as SessionType

from src.core.models.hr.position import Position as DbPosition
from src.core.schemas.hr.position import Position


def get_all(session: SessionType):
    stmnt = select(DbPosition)

    result = session.exec(stmnt)
    return result.all()


def get_by_id(position_id: str, session: SessionType):
    stmnt = select(DbPosition).where(DbPosition.id == position_id)

    result = session.exec(stmnt)
    return result.first()


def create(position: DbPosition, session: SessionType):
    try:
        session.add(position)
        session.commit()
        session.refresh(position)
        return Position.model_validate(position)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def update(position: DbPosition, session: SessionType):
    try:
        session.commit()
        session.refresh(position)
        return Position.model_validate(position)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    

def delete(position: DbPosition, session: SessionType):
    try:
        session.delete(position)
        session.commit()
        return {"message": f"Position with id {position.id} deleted successfully"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
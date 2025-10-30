from fastapi import HTTPException
from sqlmodel import select
from sqlalchemy.orm import Session as SessionType

from src.core.models.hr.position import Position as DbPosition
from src.core.schemas.hr.position import Position


def get_all(session):
    stmnt = select(DbPosition)

    result = session.execute(stmnt)
    return result.scalars().all()


def get_by_id(position_id: str, session):
    stmnt = select(DbPosition).where(DbPosition.id == position_id)

    result = session.execute(stmnt)
    return result.scalar_one_or_none()


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
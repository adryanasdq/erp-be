from fastapi import HTTPException
from sqlmodel import select, Session as SessionType

from src.core.models.inventory.stock_movement import StockMovement as DbStockMovement
from src.core.schemas.inventory.stock_movement import StockMovement


def get_all(session: SessionType):
    stmnt = select(DbStockMovement)

    result = session.exec(stmnt)
    return result.all()


def get_by_id(stock_movement_id: str, session: SessionType):
    stmnt = select(DbStockMovement).where(DbStockMovement.id == stock_movement_id)

    result = session.exec(stmnt)
    return result.first()


def create(item: DbStockMovement, session: SessionType):
    try:
        session.add(item)
        session.commit()
        session.refresh(item)
        return StockMovement.model_validate(item)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
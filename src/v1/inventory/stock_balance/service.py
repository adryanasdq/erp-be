from fastapi import HTTPException
from sqlmodel import select, Session as SessionType

from src.core.models.inventory.stock_balance import StockBalance as DbStockBalance
from src.core.schemas.inventory.stock_balance import StockBalance


def get_all(session: SessionType):
    stmnt = select(DbStockBalance)

    result = session.exec(stmnt)
    return result.all()


def get_by_id(stock_balance_id: str, session: SessionType):
    stmnt = select(DbStockBalance).where(DbStockBalance.id == stock_balance_id)

    result = session.exec(stmnt)
    return result.first()


def create(item: DbStockBalance, session: SessionType):
    try:
        session.add(item)
        session.commit()
        session.refresh(item)
        return StockBalance.model_validate(item)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def update(item: DbStockBalance, session: SessionType):
    try:
        session.commit()
        session.refresh(item)
        return StockBalance.model_validate(item)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
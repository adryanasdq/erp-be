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

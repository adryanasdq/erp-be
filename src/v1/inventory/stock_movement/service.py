from fastapi import HTTPException
from sqlmodel import select, Session as SessionType

from src.core.models.inventory.stock_movement import StockMovement as DbStockMovement
from src.core.schemas.inventory.stock_movement import StockMovement

from src.core.models.inventory.stock_balance import StockBalance as DbStockBalance
from src.core.schemas.inventory.stock_balance import StockBalance


def get_all(session: SessionType):
    stmnt = select(DbStockMovement)

    result = session.exec(stmnt)
    return result.all()


def get_by_id(stock_movement_id: str, session: SessionType):
    stmnt = select(DbStockMovement).where(DbStockMovement.id == stock_movement_id)

    result = session.exec(stmnt)
    return result.first()


def create(movement: DbStockMovement, balance: DbStockBalance, session: SessionType):
    try:
        session.add(movement)
        session.add(balance)

        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def transfer(
    transfers: list[DbStockMovement],
    balances: list[DbStockBalance],
    session: SessionType,
):
    try:
        for i in range(2):
            session.add(transfers[i])
            session.add(balances[i])

        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))

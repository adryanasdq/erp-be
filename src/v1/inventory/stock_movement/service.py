from fastapi import HTTPException
from sqlmodel import select, Session as SessionType

from src.core.models.inventory.stock_movement import StockMovement as DbStockMovement
from src.core.schemas.inventory.stock_movement import StockMovement

from src.core.models.inventory.stock_balance import StockBalance as DBStockBalance
from src.core.schemas.inventory.stock_balance import StockBalance


def get_all(session: SessionType):
    stmnt = select(DbStockMovement)

    result = session.exec(stmnt)
    return result.all()


def get_by_id(stock_movement_id: str, session: SessionType):
    stmnt = select(DbStockMovement).where(DbStockMovement.id == stock_movement_id)

    result = session.exec(stmnt)
    return result.first()


def create(movement: DbStockMovement, balance: DBStockBalance, session: SessionType):
    try:
        session.add(movement)
        session.add(balance)

        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    

# def transfer(movements: list[DbStockMovement], session: SessionType):
#     try:
#         for movement in movements:
#             session.add(movement)
        
#         session.commit()
#     except Exception as e:
#         session.rollback()
#         raise HTTPException(status_code=400, detail=str(e))

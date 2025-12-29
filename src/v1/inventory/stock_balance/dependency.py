from datetime import datetime
from sqlmodel import select, Session as SessionType

from src.core.models.inventory.stock_balance import StockBalance as DbStockBalance
from src.core.schemas.inventory.stock_movement import StockMovement

from .exception import StockBalanceInsufficent


def get_stock_balance(item_id: str, warehouse_id: str, session: SessionType):
    stmnt = select(DbStockBalance).where(
        DbStockBalance.item_id == item_id, DbStockBalance.warehouse_id == warehouse_id
    )
    query = session.exec(stmnt)
    db_stock_balance = query.first()

    return db_stock_balance


def validate_stock_balance(stock_movement: StockMovement, session: SessionType):
    db_stock_balance = get_stock_balance(
        stock_movement.item_id, stock_movement.warehouse_id, session
    )

    if not db_stock_balance:
        db_stock_balance = DbStockBalance(
            item_id=stock_movement.item_id,
            warehouse_id=stock_movement.warehouse_id,
            qty=stock_movement.qty,
            qty_reserved=0,
        )
    else:
        #TODO: need to convert uom

        if stock_movement.type == "in":
            db_stock_balance.qty += stock_movement.qty

        if stock_movement.type == "out":
            if db_stock_balance.qty < stock_movement.qty:
                raise StockBalanceInsufficent()
            
            db_stock_balance.qty -= stock_movement.qty

        if stock_movement.type == "adj":
            db_stock_balance.qty = stock_movement.qty

    db_stock_balance.modified_date = datetime.now()
    return db_stock_balance
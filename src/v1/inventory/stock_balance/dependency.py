from datetime import datetime
from fastapi import Depends
from sqlmodel import Session as SessionType

from src.core.settings.database import get_session
from src.core.models.inventory.stock_balance import StockBalance as DbStockBalance
from src.core.schemas.inventory.stock_balance import StockBalance

from .exception import StockBalanceIdExists, StockBalanceNotFound
from ..item.dependency import get_item_by_id
from ..warehouse.dependency import get_warehouse_by_id


def check_if_stock_balance_exists(stock_balance_id: str, session: SessionType):
    db_stock_balance = session.get(DbStockBalance, stock_balance_id)
    if db_stock_balance:
        raise StockBalanceIdExists()
    return


def get_stock_balance_by_id(
    id: str, session: SessionType = Depends(get_session)
):
    db_stock_balance = session.get(DbStockBalance, id)
    if not db_stock_balance:
        raise StockBalanceNotFound()
    return db_stock_balance


def validate_stock_balance(stock_balance: StockBalance, session: SessionType, id: str = None):
    get_item_by_id(stock_balance.item_id)
    get_warehouse_by_id(stock_balance.warehouse_id)

    if not id:
        db_stock_balance = DbStockBalance(
            **stock_balance.model_dump(exclude_unset=True, exclude={"id"})
        )
    else:
        db_stock_balance = get_stock_balance_by_id(id, session)
        for key, attr in stock_balance.model_dump(exclude_unset=True).items():
            setattr(db_stock_balance, key, attr)

    db_stock_balance.modified_date = datetime.now()
    return db_stock_balance
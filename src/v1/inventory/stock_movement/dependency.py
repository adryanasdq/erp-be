from datetime import datetime
from fastapi import Depends
from sqlmodel import Session as SessionType

from src.core.settings.database import get_session
from src.core.models.inventory.stock_movement import StockMovement as DbStockMovement
from src.core.schemas.inventory.stock_movement import StockMovement

from .exception import StockMovementIdExists
from ..item.dependency import get_item_by_id
from ..warehouse.dependency import get_warehouse_by_id
from ..unit_of_measure.dependency import get_uom_by_id


def check_if_stock_movement_exists(stock_movement_id: str, session: SessionType):
    db_stock_movement = session.get(DbStockMovement, stock_movement_id)
    if db_stock_movement:
        raise StockMovementIdExists()
    return


def validate_stock_movement(stock_movement: StockMovement, session: SessionType):
    get_item_by_id(stock_movement.item_id, session)
    get_warehouse_by_id(stock_movement.warehouse_id, session)
    get_uom_by_id(stock_movement.uom_id, session)

    db_stock_movement = DbStockMovement(
        **stock_movement.model_dump(exclude_unset=True, exclude={"id"})
    )

    return db_stock_movement
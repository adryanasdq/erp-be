from datetime import datetime
from sqlmodel import Session as SessionType

from src.core.models.inventory.stock_movement import StockMovement as DbStockMovement
from src.core.schemas.inventory.stock_movement import StockMovement, StockTransfer

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

    db_stock_movement.created_date = datetime.now()

    return db_stock_movement


def validate_stock_transfer(stock_transfer: StockTransfer, session: SessionType):
    get_item_by_id(stock_transfer.item_id, session)
    get_warehouse_by_id(stock_transfer.from_warehouse_id, session)
    get_warehouse_by_id(stock_transfer.to_warehouse_id, session)
    get_uom_by_id(stock_transfer.uom_id, session)

    db_stock_transfers = []
    db_transfer_out = DbStockMovement(
        type="out",
        warehouse_id=stock_transfer.from_warehouse_id,
        **stock_transfer.model_dump(
            exclude_unset=True, exclude={"id", "from_warehouse_id", "to_warehouse_id"}
        ),
    )

    db_transfer_in = DbStockMovement(
        type="in",
        warehouse_id=stock_transfer.to_warehouse_id,
        **stock_transfer.model_dump(
            exclude_unset=True, exclude={"id", "from_warehouse_id", "to_warehouse_id"}
        ),
    )

    db_stock_transfers.append(db_transfer_out)
    db_stock_transfers.append(db_transfer_in)

    return db_stock_transfers

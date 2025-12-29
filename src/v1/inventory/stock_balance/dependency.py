from datetime import datetime
from sqlmodel import select, Session as SessionType

from src.core.models.inventory.stock_balance import StockBalance as DbStockBalance
from src.core.schemas.inventory.stock_movement import StockMovement, StockTransfer

from src.v1.inventory.item_uom_conversion.dependency import get_conv_factor_to_base

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

    factor = get_conv_factor_to_base(
        stock_movement.item_id, stock_movement.uom_id, session
    )
    converted_qty = stock_movement.qty * factor

    if not db_stock_balance:
        db_stock_balance = DbStockBalance(
            item_id=stock_movement.item_id,
            warehouse_id=stock_movement.warehouse_id,
            qty=converted_qty,
            qty_reserved=0,
        )
    else:
        if stock_movement.type == "in":
            db_stock_balance.qty += converted_qty

        if stock_movement.type == "out":
            if db_stock_balance.qty < converted_qty:
                raise StockBalanceInsufficent()

            db_stock_balance.qty -= converted_qty

        if stock_movement.type == "adj":
            db_stock_balance.qty = converted_qty

    db_stock_balance.modified_date = datetime.now()
    return db_stock_balance


def validate_balance_transfer(stock_transfer: StockTransfer, session: SessionType):
    db_stock_balances = []
    db_stock_balance_out = get_stock_balance(
        stock_transfer.item_id, stock_transfer.from_warehouse_id, session
    )

    db_stock_balance_in = get_stock_balance(
        stock_transfer.item_id, stock_transfer.to_warehouse_id, session
    )

    factor = get_conv_factor_to_base(
        stock_transfer.item_id, stock_transfer.uom_id, session
    )
    converted_qty = stock_transfer.qty * factor

    if db_stock_balance_out.qty < converted_qty:
        raise StockBalanceInsufficent()

    db_stock_balance_out.qty -= converted_qty
    db_stock_balance_in.qty += converted_qty

    db_stock_balances.append(db_stock_balance_out)
    db_stock_balances.append(db_stock_balance_in)

    return db_stock_balances

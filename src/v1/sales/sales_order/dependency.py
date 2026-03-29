from datetime import datetime
from sqlmodel import Session as SessionType, select
from src.core.models.sales.sales_order import SalesOrder as DbSO, SalesOrderLine as DbSOLine
from src.core.models.inventory.stock_balance import StockBalance as DbBalance
from src.core.schemas.sales.sales_order import SalesOrderSchema
from src.v1.inventory.item_uom_conversion.dependency import get_conv_factor_to_base

from .exception import SONotFound, SONumberExists, SOInsufficientStock, SOInvalidStatus


def get_so_by_id(so_id: str, session: SessionType):
    db_so = session.get(DbSO, so_id)
    if not db_so:
        from .exception import SONotFound
        raise SONotFound()
    return db_so

def validate_so_creation(data: SalesOrderSchema, session: SessionType):
    # Check if SO Number is unique
    existing = session.exec(select(DbSO).where(DbSO.so_number == data.so_number)).first()
    if existing:
        raise SONumberExists()

    db_so = DbSO(**data.model_dump(exclude={"lines"}))
    db_so.lines = [DbSOLine(**line.model_dump()) for line in data.lines]
    db_so.modified_date = datetime.now()
    return db_so

def validate_so_confirmation(so_id: str, session: SessionType):
    db_so = session.get(DbSO, so_id)
    if not db_so:
        raise SONotFound()
    if db_so.status != "DRAFT":
        raise SOInvalidStatus(db_so.status)

    # Process Reservation Logic
    for line in db_so.lines:
        factor = get_conv_factor_to_base(line.item_id, line.uom_id, session)
        base_qty = line.qty_ordered * factor
        
        # Check Balance
        stmnt = select(DbBalance).where(
            DbBalance.item_id == line.item_id,
            DbBalance.warehouse_id == db_so.warehouse_id
        )
        balance = session.exec(stmnt).first()
        
        available_qty = (balance.qty - balance.qty_reserved) if balance else 0
        
        if available_qty < base_qty:
            raise SOInsufficientStock(line.item_id, available_qty)
            
        # Stage the reservation update
        balance.qty_reserved += base_qty
        
    db_so.status = "CONFIRMED"
    db_so.modified_date = datetime.now()
    return db_so
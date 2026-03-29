from fastapi import HTTPException
from sqlmodel import select, Session as SessionType

from .dependency import get_so_by_id

from src.core.models.inventory.stock_balance import StockBalance as DbBalance
from src.v1.inventory.item_uom_conversion.dependency import get_conv_factor_to_base

def confirm_so(so_id: str, session: SessionType):
    db_so = get_so_by_id(so_id, session) 
    for line in db_so.lines:
        factor = get_conv_factor_to_base(line.item_id, line.uom_id, session)
        base_qty = line.qty_ordered * factor
        
        stmnt = select(DbBalance).where(
            DbBalance.item_id == line.item_id,
            DbBalance.warehouse_id == db_so.warehouse_id
        )
        balance = session.exec(stmnt).first()
        
        available_qty = (balance.qty - balance.qty_reserved) if balance else 0
        
        if available_qty < base_qty:
            raise HTTPException(
                status_code=400, 
                detail=f"Insufficient stock for item {line.item_id}. "
                       f"Available: {available_qty}"
            )
            
        balance.qty_reserved += base_qty
        
    db_so.status = "CONFIRMED"
    session.commit()
    return db_so
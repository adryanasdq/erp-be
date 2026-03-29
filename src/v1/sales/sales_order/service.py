from fastapi import HTTPException
from sqlmodel import select, Session as SessionType
from src.core.models.sales.sales_order import SalesOrder as DbSO
from src.core.models.inventory.stock_balance import StockBalance as DbBalance
from src.v1.inventory.item_uom_conversion.dependency import get_conv_factor_to_base

def confirm_so(so_id: str, session: SessionType):
    db_so = session.get(DbSO, so_id)
    if not db_so:
        raise HTTPException(status_code=404, detail="SO not found")
    
    if db_so.status != "DRAFT":
        raise HTTPException(status_code=400, detail="Only DRAFT orders can be confirmed")

    try:
        for line in db_so.lines:
            # 1. Convert to Base Qty
            factor = get_conv_factor_to_base(line.item_id, line.uom_id, session)
            base_qty = line.qty_ordered * factor
            
            # 2. Check Availability
            stmnt = select(DbBalance).where(
                DbBalance.item_id == line.item_id,
                DbBalance.warehouse_id == db_so.warehouse_id
            )
            balance = session.exec(stmnt).first()
            
            if not balance or (balance.qty_on_hand - balance.qty_reserved) < base_qty:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Insufficient stock for item {line.item_id}"
                )
            
            # 3. Reserve the stock
            balance.qty_reserved += base_qty
            
        db_so.status = "CONFIRMED"
        session.commit()
        session.refresh(db_so)
        return db_so
    except Exception as e:
        session.rollback()
        raise e
from fastapi import HTTPException
from sqlmodel import Session as SessionType

from src.core.models.purchasing.goods_receipt import GoodsReceipt as DbGRN
from src.core.models.inventory.stock_movement import StockMovement
from src.v1.inventory.item_uom_conversion.dependency import get_conv_factor_to_base


def create(grn: DbGRN, session: SessionType):
    try:
        # 1. Save the Goods Receipt header and lines
        session.add(grn)
        
        # 2. Process each line for Stock Movement
        for line in grn.lines:
            # Get the conversion factor to Base UOM
            factor = get_conv_factor_to_base(line.item_id, line.uom_id, session)
            base_qty = line.qty * factor
            
            movement = StockMovement(
                item_id=line.item_id,
                warehouse_id=grn.warehouse_id,
                qty=base_qty,
                type="IN",
                reference=f"GRN-{grn.id[:8]}", # Using a slice of CUID as ref
                movement_date=grn.received_date
            )
            session.add(movement)
            
        # 3. Commit as an atomic transaction
        session.commit()
        session.refresh(grn)
        return grn
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def get_all(session: SessionType):
    from sqlmodel import select
    stmnt = select(DbGRN)
    return session.exec(stmnt).all()


def get_by_id(grn_id: str, session: SessionType):
    return session.get(DbGRN, grn_id)
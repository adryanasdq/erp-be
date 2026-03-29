from fastapi import HTTPException
from sqlmodel import Session as SessionType, select

from src.core.models.purchasing.goods_receipt import GoodsReceipt as DbGRN
from src.core.models.inventory.stock_movement import StockMovement
from src.v1.inventory.item_uom_conversion.dependency import get_conv_factor_to_base
from src.core.models.inventory.stock_balance import StockBalance as DbBalance


def create(grn: DbGRN, session: SessionType):
    try:
        session.add(grn)
        
        for line in grn.lines:
            factor = get_conv_factor_to_base(line.item_id, line.uom_id, session)
            base_qty = line.qty * factor
            
            # 1. Create Movement (The Ledger)
            movement = StockMovement(
                item_id=line.item_id,
                warehouse_id=grn.warehouse_id,
                qty=base_qty,
                type="IN",
                reference=f"GRN-{grn.id[:8]}"
            )
            session.add(movement)
            
            # 2. Update Balance (The Current Total)
            stmnt = select(DbBalance).where(
                DbBalance.item_id == line.item_id,
                DbBalance.warehouse_id == grn.warehouse_id
            )
            balance = session.exec(stmnt).first()
            
            if not balance:
                # First time this item hits this warehouse
                balance = DbBalance(
                    item_id=line.item_id,
                    warehouse_id=grn.warehouse_id,
                    qty_on_hand=base_qty,
                    qty_reserved=0.0
                )
                session.add(balance)
            else:
                balance.qty_on_hand += base_qty

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
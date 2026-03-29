from fastapi import HTTPException
from sqlmodel import Session as SessionType
from src.core.models.purchasing.goods_receipt import GoodsReceipt as DbGRN

from src.v1.inventory.stock_movement.service import create as create_movement
from src.v1.inventory.stock_balance.dependency import validate_stock_balance
from src.v1.inventory.stock_movement.dependency import validate_stock_movement
from src.core.schemas.inventory.stock_movement import StockMovement as StockMovementSchema

def create(grn: DbGRN, session: SessionType):
    try:
        session.add(grn)
        
        for line in grn.lines:
            movement_data = StockMovementSchema(
                item_id=line.item_id,
                warehouse_id=grn.warehouse_id,
                qty=line.qty,
                uom_id=line.uom_id,
                type="in",
                reference=f"GRN-{grn.id[:8]}"
            )
            
            db_movement = validate_stock_movement(movement_data, session)
            db_balance = validate_stock_balance(movement_data, session)
            
            create_movement(db_movement, db_balance, session)
            
        session.commit()
        session.refresh(grn)
        return grn
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
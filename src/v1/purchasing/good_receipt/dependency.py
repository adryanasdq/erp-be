from datetime import datetime
from sqlmodel import Session as SessionType
from src.core.models.purchasing.goods_receipt import GoodsReceipt as DbGRN, GoodsReceiptLine as DbGRNLine
from src.core.schemas.purchasing.goods_receipt import GoodsReceiptSchema

from src.v1.inventory.stock_movement.dependency import validate_stock_movement
from src.v1.inventory.stock_balance.dependency import validate_stock_balance
from src.core.schemas.inventory.stock_movement import StockMovement as StockMovementSchema

from ..purchase_order.dependency import get_po_by_id
from .exception import PONotApproved

def validate_grn_processing(data: GoodsReceiptSchema, session: SessionType):
    # 1. Validate Parent PO Status
    db_po = get_po_by_id(data.po_id, session)
    if db_po.status != "APPROVED":
        raise PONotApproved()

    # 2. Prepare GRN DB Objects
    db_grn = DbGRN(**data.model_dump(exclude={"lines"}))
    db_grn.lines = [DbGRNLine(**line.model_dump()) for line in data.lines]
    
    # 3. Prepare Inventory Updates
    inventory_updates = []
    
    for line in data.lines:
        movement_schema = StockMovementSchema(
            item_id=line.item_id,
            warehouse_id=data.warehouse_id,
            qty=line.qty,
            uom_id=line.uom_id,
            type="in",
            reference=f"GRN-{db_grn.id[:8]}"
        )
        
        # Pre-calculate movement and balance using your Inventory Dependencies
        db_mov = validate_stock_movement(movement_schema, session)
        db_bal = validate_stock_balance(movement_schema, session)
        
        inventory_updates.append((db_mov, db_bal))

    return {
        "grn": db_grn,
        "inventory_updates": inventory_updates
    }
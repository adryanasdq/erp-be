from datetime import datetime
from sqlmodel import Session as SessionType
from src.core.models.sales.delivery import Delivery as DbDelivery, DeliveryLine as DbDeliveryLine
from src.core.schemas.sales.delivery import DeliverySchema

# Inventory Integration
from src.v1.inventory.stock_movement.dependency import validate_stock_movement
from src.v1.inventory.stock_balance.dependency import validate_stock_balance
from src.core.schemas.inventory.stock_movement import StockMovement as StockMovementSchema

from ..sales_order.dependency import get_so_by_id
from .exception import SODeliveryNotConfirmed

def validate_delivery_processing(data: DeliverySchema, session: SessionType):
    # 1. Validate Parent SO Status
    db_so = get_so_by_id(data.so_id, session)
    if db_so.status not in ["CONFIRMED", "PARTIALLY_DELIVERED"]:
        raise SODeliveryNotConfirmed()

    # 2. Prepare Delivery DB Objects
    db_delivery = DbDelivery(**data.model_dump(exclude={"lines"}))
    db_delivery.lines = [DbDeliveryLine(**line.model_dump()) for line in data.lines]
    db_delivery.delivery_date = datetime.now()
    
    # 3. Prepare Inventory Updates (The Stock OUT logic)
    inventory_updates = []
    
    for line in data.lines:
        movement_schema = StockMovementSchema(
            item_id=line.item_id,
            warehouse_id=data.warehouse_id,
            qty=line.qty,
            uom_id=line.uom_id,
            type="out", # Triggers the qty and qty_reserved reduction
            reference=f"DO-{db_delivery.id[:8]}"
        )
        
        # Pre-process via your Inventory Logic
        db_mov = validate_stock_movement(movement_schema, session)
        db_bal = validate_stock_balance(movement_schema, session)
        
        inventory_updates.append((db_mov, db_bal))
        
        # 4. Update SO Line delivered quantity (Optional but recommended)
        for so_line in db_so.lines:
            if so_line.item_id == line.item_id:
                so_line.qty_delivered += line.qty

    # Update SO Status based on fulfillment
    all_done = all(l.qty_delivered >= l.qty_ordered for l in db_so.lines)
    db_so.status = "DELIVERED" if all_done else "PARTIALLY_DELIVERED"

    return {
        "delivery": db_delivery,
        "inventory_updates": inventory_updates
    }
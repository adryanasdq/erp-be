from datetime import datetime
from sqlmodel import Session as SessionType
from src.core.models.sales.delivery import Delivery as DbDelivery, DeliveryLine as DbDeliveryLine
from src.core.schemas.sales.delivery import DeliverySchema
from src.v1.inventory.stock_movement.dependency import validate_stock_movement
from src.v1.inventory.stock_balance.dependency import validate_stock_balance
from src.core.schemas.inventory.stock_movement import StockMovement as StockMovementSchema
from ..sales_order.dependency import get_so_by_id
from .exception import SODeliveryNotConfirmed

def validate_delivery_processing(data: DeliverySchema, session: SessionType):
    # 1. Validation Logic
    db_so = get_so_by_id(data.so_id, session)
    if db_so.status not in ["CONFIRMED", "PARTIALLY_DELIVERED"]:
        raise SODeliveryNotConfirmed()

    # 2. Prepare Delivery Objects
    db_delivery = DbDelivery(**data.model_dump(exclude={"lines"}))
    db_delivery.lines = [DbDeliveryLine(**line.model_dump()) for line in data.lines]
    
    # 3. Prepare Inventory Objects (Movements + Updated Balances)
    # This list will be passed to service.py for the final commit
    inventory_updates = [] 
    
    for line in data.lines:
        movement_schema = StockMovementSchema(
            item_id=line.item_id,
            warehouse_id=data.warehouse_id,
            qty=line.qty,
            uom_id=line.uom_id,
            type="out",
            reference=f"DO-{db_delivery.id[:8]}"
        )
        
        # Pre-process the movement and balance via your Inventory Dependencies
        db_mov = validate_stock_movement(movement_schema, session)
        db_bal = validate_stock_balance(movement_schema, session)
        
        inventory_updates.append((db_mov, db_bal))

    # Return everything needed for the transaction
    return {
        "delivery": db_delivery,
        "inventory_updates": inventory_updates
    }
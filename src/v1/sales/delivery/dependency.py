from datetime import datetime
from sqlmodel import Session as SessionType, select
from src.core.models.sales.delivery import (
    Delivery as DbDelivery,
    DeliveryLine as DbDeliveryLine,
)
from src.core.schemas.accounting.journal import JournalEntrySchema, JournalLineSchema
from src.core.schemas.sales.delivery import DeliverySchema

from src.v1.accounting.journal.dependency import (
    get_account_by_code,
    validate_journal_entry,
)
from src.v1.inventory.stock_movement.dependency import validate_stock_movement
from src.v1.inventory.stock_balance.dependency import validate_stock_balance
from src.core.schemas.inventory.stock_movement import (
    StockMovement as StockMovementSchema,
)

from ..sales_order.dependency import get_so_by_id
from .exception import DeliveryNotFound, SODeliveryNotConfirmed


def get_delivery_by_id(delivery_id: str, session: SessionType):
    delivery = session.get(DbDelivery, delivery_id)
    if not delivery:
        raise DeliveryNotFound()
    return delivery


def get_all_deliveries(session: SessionType, so_id: str = None):
    statement = select(DbDelivery)
    if so_id:
        statement = statement.where(DbDelivery.so_id == so_id)

    return session.exec(statement).all()


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
            type="out",  # Triggers the qty and qty_reserved reduction
            reference=f"DO-{db_delivery.id[:8]}",
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

    # 4. Calculate COGS (Cost of Goods Sold)
    # Usually based on the Weighted Average Cost of the item
    total_cost = sum(line.qty * 60 for line in data.lines)  # Example: Cost is $60/unit

    # 5. Prepare COGS Journal
    # Logic: Dr COGS (5010), Cr Inventory (1010)
    cogs_account = get_account_by_code("5010", session)
    inv_account = get_account_by_code("1010", session)

    journal_data = JournalEntrySchema(
        reference_type="DELIVERY",
        reference_id=db_delivery.id,
        description=f"COGS for Delivery {db_delivery.id[:8]}",
        lines=[
            JournalLineSchema(account_id=cogs_account.id, debit=total_cost),
            JournalLineSchema(account_id=inv_account.id, credit=total_cost),
        ],
    )

    db_journal = validate_journal_entry(journal_data, session)

    return {
        "delivery": db_delivery,
        "inventory_updates": inventory_updates,
        "journal_entry": db_journal,
    }

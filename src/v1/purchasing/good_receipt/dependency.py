from datetime import datetime
from sqlmodel import Session as SessionType, select
from src.core.models.purchasing.goods_receipt import (
    GoodsReceipt as DbGRN,
    GoodsReceiptLine as DbGRNLine,
)
from src.core.schemas.accounting.journal import JournalEntrySchema, JournalLineSchema
from src.core.schemas.purchasing.goods_receipt import GoodsReceiptSchema

from src.v1.accounting.journal.dependency import (
    get_account_by_code,
    validate_journal_entry,
)
from src.v1.inventory.stock_movement.dependency import validate_stock_movement
from src.v1.inventory.stock_balance.dependency import validate_stock_balance
from src.core.schemas.inventory.stock_movement import (
    StockMovement as StockMovementSchema,
)

from ..purchase_order.dependency import get_po_by_id
from .exception import PONotApproved, GRNNotFound, GRNAlreadyCanceled


def get_grn_by_id(grn_id: str, session: SessionType):
    grn = session.get(DbGRN, grn_id)
    if not grn:
        raise GRNNotFound()
    return grn


def get_all_grns(session: SessionType, po_id: str = None):
    statement = select(DbGRN)
    if po_id:
        statement = statement.where(DbGRN.po_id == po_id)
    return session.exec(statement).all()


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
            reference=f"GRN-{db_grn.id[:8]}",
        )

        # Pre-calculate movement and balance using your Inventory Dependencies
        db_mov = validate_stock_movement(movement_schema, session)
        db_bal = validate_stock_balance(movement_schema, session)

        inventory_updates.append((db_mov, db_bal))

    # 4. Calculate Total Value for Accounting
    # In real life, you'd pull the price from the PO Line
    total_value = sum(line.qty * 100 for line in data.lines)  # Example: $100/unit

    # 5. Prepare Journal Entry
    # Logic: Dr Inventory (1010), Cr Accounts Payable (2010)
    inv_account = get_account_by_code("1010", session)  # Inventory Account
    ap_account = get_account_by_code("2010", session)  # AP Account

    journal_data = JournalEntrySchema(
        reference_type="GRN",
        reference_id=db_grn.id,
        description=f"Automated entry for GRN {db_grn.id[:8]}",
        lines=[
            JournalLineSchema(account_id=inv_account.id, debit=total_value),
            JournalLineSchema(account_id=ap_account.id, credit=total_value),
        ],
    )

    db_journal = validate_journal_entry(journal_data, session)

    return {
        "grn": db_grn,
        "inventory_updates": inventory_updates,
        "journal_entry": db_journal,
    }


def validate_grn_cancellation(grn_id: str, session: SessionType):
    db_grn = get_grn_by_id(grn_id, session)

    # 1. Prepare Inventory Reversal (Stock OUT)
    inventory_reversals = []
    for line in db_grn.lines:
        movement_schema = StockMovementSchema(
            item_id=line.item_id,
            warehouse_id=db_grn.warehouse_id,
            qty=line.qty,
            uom_id=line.uom_id,
            type="out",  # Reversing the previous 'in'
            reference=f"VOID-{db_grn.id[:8]}",
        )
        db_mov = validate_stock_movement(movement_schema, session)
        db_bal = validate_stock_balance(movement_schema, session)
        inventory_reversals.append((db_mov, db_bal))

    db_grn.status = "CANCELED"
    return db_grn, inventory_reversals


def validate_grn_cancellation(grn_id: str, session: SessionType):
    # 1. Fetch and Validate State
    db_grn = get_grn_by_id(grn_id, session)

    if db_grn.status == "CANCELED":
        raise GRNAlreadyCanceled()

    # 2. Prepare Inventory Reversal (The "Undo" Engine)
    # We must create a 'Stock OUT' for every line that was originally 'IN'
    inventory_reversals = []

    for line in db_grn.lines:
        movement_schema = StockMovementSchema(
            item_id=line.item_id,
            warehouse_id=db_grn.warehouse_id,
            qty=line.qty,
            uom_id=line.uom_id,
            type="out",  # This is the "Mirror": original was 'in', reversal is 'out'
            reference=f"VOID-{db_grn.grn_number}",
        )

        # Call your existing inventory logic to prepare the DB objects
        db_mov = validate_stock_movement(movement_schema, session)
        db_bal = validate_stock_balance(movement_schema, session)

        inventory_reversals.append((db_mov, db_bal))

    # 3. Update GRN Status
    db_grn.status = "CANCELED"
    db_grn.modified_date = datetime.now()

    return {"grn": db_grn, "inventory_reversals": inventory_reversals}

from datetime import datetime
from fastapi import Depends
from sqlmodel import Session as SessionType
from src.core.settings.database import get_session
from src.core.models.purchasing.goods_receipt import GoodsReceipt as DbGRN, GoodsReceiptLine as DbGRNLine
from src.core.schemas.purchasing.goods_receipt import GoodsReceiptSchema

# Cross-module validation
from ..purchase_order.dependency import get_po_by_id
from ...inventory.warehouse.dependency import get_warehouse_by_id # Assuming this exists

def validate_grn(data: GoodsReceiptSchema, session: SessionType):
    # Verify PO and Warehouse exist
    get_po_by_id(data.po_id, session)
    get_warehouse_by_id(data.warehouse_id, session)

    db_grn = DbGRN(**data.model_dump(exclude={"lines"}))
    
    db_lines = []
    for line in data.lines:
        db_lines.append(DbGRNLine(**line.model_dump()))
    
    db_grn.lines = db_lines
    db_grn.modified_date = datetime.now()
    return db_grn
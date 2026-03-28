from datetime import datetime
from fastapi import Depends
from sqlmodel import Session as SessionType, select

from src.core.settings.database import get_session
from src.core.models.purchasing.purchase_order import PurchaseOrder as DbPO, PurchaseOrderLine as DbPOLine
from src.core.schemas.purchasing.purchase_order import PurchaseOrderSchema

# Cross-module dependencies following your pattern
from ..supplier.dependency import get_supplier_by_id
from ...inventory.item.dependency import get_item_by_id
from ...inventory.unit_of_measure.dependency import get_uom_by_id
from .exception import PONotFound, PONumberExists


def get_po_by_id(id: str, session: SessionType = Depends(get_session)):
    db_po = session.get(DbPO, id)
    if not db_po:
        raise PONotFound()
    return db_po


def validate_po(data: PurchaseOrderSchema, session: SessionType, id: str = None):
    # 1. Ensure Supplier exists
    get_supplier_by_id(data.supplier_id, session)

    if not id:
        # CREATE FLOW
        # Check for unique PO Number
        existing = session.exec(select(DbPO).where(DbPO.po_number == data.po_number)).first()
        if existing:
            raise PONumberExists()

        # Map Header
        db_po = DbPO(**data.model_dump(exclude={"id", "lines"}))
        
        # Map Lines & Validate Items/UOMs
        db_lines = []
        for line in data.lines:
            get_item_by_id(line.item_id, session)
            get_uom_by_id(line.uom_id, session)
            db_lines.append(DbPOLine(**line.model_dump()))
        
        db_po.lines = db_lines
    
    else:
        # UPDATE FLOW
        db_po = get_po_by_id(id, session)
        
        # Update Header attributes
        header_data = data.model_dump(exclude_unset=True, exclude={"id", "lines"})
        for key, attr in header_data.items():
            setattr(db_po, key, attr)
            
        # Note: ERP line updates are usually complex (delete/re-insert or sync).
        # For now, we update the header. If you want to sync lines, let me know.

    db_po.modified_date = datetime.now()
    return db_po
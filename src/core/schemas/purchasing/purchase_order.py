from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime

class PurchaseOrderLineSchema(BaseModel):
    item_id: str
    qty: float
    uom_id: str
    price: float

    model_config = {"from_attributes": True}

class PurchaseOrderSchema(BaseModel):
    id: Optional[str] = Field(None, readonly=True)
    po_number: str
    supplier_id: str
    status: str = "DRAFT"
    order_date: Optional[datetime] = None
    lines: List[PurchaseOrderLineSchema] = []

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "po_number": "PO-2026-001",
                "supplier_id": "cuid_here",
                "status": "DRAFT",
                "lines": [
                    {
                        "item_id": "item_cuid",
                        "qty": 10.0,
                        "uom_id": "uom_cuid",
                        "price": 150.0
                    }
                ]
            }
        }
    }
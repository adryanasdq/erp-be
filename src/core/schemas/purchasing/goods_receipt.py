from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime

class GoodsReceiptLineSchema(BaseModel):
    item_id: str
    qty: float
    uom_id: str

    model_config = {"from_attributes": True}

class GoodsReceiptSchema(BaseModel):
    id: Optional[str] = Field(None, readonly=True)
    po_id: str
    warehouse_id: str
    received_date: Optional[datetime] = None
    lines: List[GoodsReceiptLineSchema]

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "po_id": "po_cuid_123",
                "warehouse_id": "wh_cuid_456",
                "lines": [
                    {
                        "item_id": "item_cuid_789",
                        "qty": 50.0,
                        "uom_id": "uom_cuid_000"
                    }
                ]
            }
        }
    }
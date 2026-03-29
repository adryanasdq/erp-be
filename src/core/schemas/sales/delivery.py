from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime

class DeliveryLineSchema(BaseModel):
    item_id: str
    qty: float
    uom_id: str

    model_config = {"from_attributes": True}

class DeliverySchema(BaseModel):
    id: Optional[str] = Field(None, readonly=True)
    so_id: str
    warehouse_id: str
    delivery_date: Optional[datetime] = None
    lines: List[DeliveryLineSchema]

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "so_id": "so_cuid_123",
                "warehouse_id": "wh_cuid_456",
                "lines": [
                    {
                        "item_id": "item_cuid_789",
                        "qty": 5.0,
                        "uom_id": "uom_cuid_000"
                    }
                ]
            }
        }
    }
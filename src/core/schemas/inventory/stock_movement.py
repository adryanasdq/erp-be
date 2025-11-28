from typing import Optional
from pydantic import BaseModel, Field


class StockMovement(BaseModel):
    id: Optional[str] = Field(None, readonly=True)
    item_id: str
    warehouse_id: str
    type: str
    qty: int
    uom_id: str

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "item_id": "sabjvbor17",
                "warehouse_id": "x1b3vmorte",
                "type": "IN",
                "qty": 5,
                "uom_id": "p2kedncndm"
            }
        }
    }
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
                "item_id": "mxpenx4lgd",
                "warehouse_id": "e4yard1uj5",
                "type": "in",
                "qty": 5,
                "uom_id": "n4h26rnl0i"
            }
        }
    }


class StockTransfer(BaseModel):
    item_id: str
    from_warehouse_id: str
    to_warehouse_id: str
    qty: int
    uom_id: str

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "item_id": "mxpenx4lgd",
                "from_warehouse_id": "e4yard1uj5",
                "to_warehouse_id": "eya110dauj",
                "qty": 2,
                "uom_id": "n4h26rnl0i"
            }
        }
    }
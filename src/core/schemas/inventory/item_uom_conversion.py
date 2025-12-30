from typing import Optional
from pydantic import BaseModel, Field
from decimal import Decimal


class ItemUOMConversion(BaseModel):
    id: Optional[str] = Field(None, readonly=True)
    item_id: str
    from_uom_id: str
    to_uom_id: str
    factor: Decimal
    is_active: bool

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "item_id": "mxpenx4lgd",
                "from_uom_id": "b67gcla6av",
                "to_uom_id": "n4h26rnl0i",
                "factor": 12,
                "is_active": True,
            }
        }
    }


class ChangeStatusConversion(BaseModel):
    is_active: bool
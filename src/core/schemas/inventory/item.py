from typing import Optional
from pydantic import BaseModel, Field


class Item(BaseModel):
    id: Optional[str] = Field(None, readonly=True)
    code: str
    name: str
    category: Optional[str] = None
    uom_id: str
    is_hidden: bool

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "code": "IE202509001",
                "name": "Laptop",
                "category": "Electronic",
                "uom_id": "sabjvbor17",
                "is_hidden": False
            }
        }
    }
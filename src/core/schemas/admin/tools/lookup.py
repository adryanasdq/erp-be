from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class Lookup(BaseModel):
    id: Optional[str] = Field(None, readonly=True)
    group_code: str
    group_desc: Optional[str]
    value: str
    label: Optional[str] = ""
    order_index: Optional[int] = 0
    is_hidden: Optional[bool] = False
    modified_date: Optional[datetime] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "group_code": "EMP_STATUS",
                "group_desc": "To determine employee current status. Used in HR -> Employee",
                "value": "active",
                "label": "Active",
                "order_index": 1,
                "is_hidden": False
            }
        },
    }

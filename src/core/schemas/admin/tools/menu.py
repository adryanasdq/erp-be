from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class Menu(BaseModel):
    id: Optional[str] = Field(None, readonly=True)
    title: str
    url: str
    icon: Optional[str] = None
    parent_id: Optional[str] = None
    order_index: Optional[int] = 0
    is_hidden: Optional[bool] = False
    modified_date: Optional[datetime] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "title": "Dashboard",
                "url": "/dashboard",
                "icon": "dashboard-icon",
                "parent_id": None,
                "order_index": 1,
                "is_hidden": False,
            }
        }
    }
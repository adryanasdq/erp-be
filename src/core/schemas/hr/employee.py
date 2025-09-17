from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime, date


class Employee(BaseModel):
    id: Optional[str] = Field(None, readonly=True)
    name: str
    position_id: str
    manager_id: Optional[str] = None
    hire_date: Optional[date] = None
    status: Optional[str] = Field("active")
    modified_date: Optional[datetime] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "name": "John Doe",
                "position_id": "POS25090006",
                "manager_id": "EMP25090006",
                "hire_date": "2023-10-01 00:00:00",
                "status": "active"
            }
        }
    }
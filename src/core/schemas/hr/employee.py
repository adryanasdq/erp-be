from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime, date


class Employee(BaseModel):
    id: Optional[str] = Field(None, readonly=True)
    email: str
    username: str
    password: str
    name: str
    position_id: str
    department_id: str
    hire_date: Optional[date] = None
    status: Optional[str] = Field("active")
    modified_date: Optional[datetime] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "email": "johndoe@example.com",
                "username": "johndoe",
                "password": "securepassword123",
                "name": "John Doe",
                "position_id": "POS1234",
                "department_id": "DEP1234",
                "hire_date": "2023-10-01 00:00:00",
                "status": "active"
            }
        }
    }
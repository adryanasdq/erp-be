from typing import Optional
from pydantic import BaseModel, Field


class Department(BaseModel):
    id: Optional[str] = Field(None, readonly=True)
    name: str
    description: Optional[str] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "name": "Human Resources",
                "description": "Handles recruitment, employee relations, and benefits.",
            }
        }
    }
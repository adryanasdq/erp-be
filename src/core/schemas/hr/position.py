from typing import Optional
from pydantic import BaseModel, Field


class Position(BaseModel):
    id: Optional[str] = Field(None, readonly=True)
    title: str
    description: Optional[str] = None
    reports_to_pos_id: Optional[str] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "title": "Software Engineer",
                "description": "Responsible for developing and maintaining software applications.",
                "reports_to_pos_id": "POS0001",
            }
        }
    }
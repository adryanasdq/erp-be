from typing import Optional
from pydantic import BaseModel, Field


class Warehouse(BaseModel):
    id: Optional[str] = Field(None, readonly=True)
    name: str
    location: Optional[str] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "name": "Warehouse A",
                "location": "Point A, Victory Road 4, Johto",
            }
        }
    }
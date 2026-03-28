from typing import Optional
from pydantic import BaseModel, Field

class Supplier(BaseModel):
    id: Optional[str] = Field(None, readonly=True)
    code: str
    name: str
    status: str = "ACTIVE"

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "code": "SUP-001",
                "name": "Global Tech Corp",
                "status": "ACTIVE"
            }
        }
    }
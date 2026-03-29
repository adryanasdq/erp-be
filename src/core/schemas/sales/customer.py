from typing import Optional
from pydantic import BaseModel, Field

class Customer(BaseModel):
    id: Optional[str] = Field(None, readonly=True)
    code: str
    name: str
    status: str = "ACTIVE"

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {"code": "CUST-001", "name": "Astra International", "status": "ACTIVE"}
        }
    }
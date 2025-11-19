from typing import Optional
from pydantic import BaseModel, Field


class UnitOfMeasure(BaseModel):
    id: Optional[str] = Field(None, readonly=True)
    name: str
    symbol: Optional[str] = None
    type: str

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "name": "Piece",
                "symbol": "pc",
                "type": "count"
            }
        }
    }
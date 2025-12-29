from typing import Optional
from pydantic import BaseModel, Field


class StockBalance(BaseModel):
    id: Optional[str] = Field(None, readonly=True)
    item_id: str
    warehouse_id: str
    qty: int
    qty_reserved: int
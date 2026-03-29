from typing import Optional, List
from pydantic import BaseModel, Field


class SalesOrderLineSchema(BaseModel):
    item_id: str
    qty_ordered: float
    uom_id: str
    price: float

    model_config = {"from_attributes": True}


class SalesOrderSchema(BaseModel):
    id: Optional[str] = Field(None, readonly=True)
    so_number: str
    customer_id: str
    warehouse_id: str
    status: str = "DRAFT"
    lines: List[SalesOrderLineSchema]

    model_config = {"from_attributes": True}
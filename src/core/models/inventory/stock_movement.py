from sqlmodel import SQLModel, Field, func
from datetime import datetime

from src.utils import generate_cuid, generate_ref_doc


class StockMovement(SQLModel, table=True):
    __tablename__ = "stock_movements"
    __table_args__ = {"schema": "main"}

    id: str = Field(primary_key=True, index=True, default_factory=generate_cuid)
    item_id: str = Field(foreign_key="main.items.id", nullable=False)
    warehouse_id: str = Field(foreign_key="main.warehouses.id", nullable=False)
    type: str = Field(nullable=False)
    qty: int = Field(nullable=False)
    uom_id: str = Field(foreign_key="main.unit_of_measure.id")
    ref: str = Field(default_factory=generate_ref_doc)
    created_date: datetime = Field(default=func.now())

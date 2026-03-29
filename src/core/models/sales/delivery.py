from sqlmodel import SQLModel, Field, func, Relationship
from datetime import datetime
from typing import List, Optional
from src.utils import generate_cuid

class Delivery(SQLModel, table=True):
    __tablename__ = "deliveries"
    __table_args__ = {"schema": "main"}

    id: str = Field(primary_key=True, index=True, default_factory=generate_cuid)
    so_id: str = Field(foreign_key="main.sales_orders.id", nullable=False)
    warehouse_id: str = Field(foreign_key="main.warehouses.id", nullable=False)
    delivery_date: datetime = Field(default=func.now())
    status: str = Field(default="COMPLETED") # Usually goes straight to completed in simple setups
    modified_date: datetime = Field(
        default=func.now(), sa_column_kwargs={"onupdate": func.now()}
    )

    lines: List["DeliveryLine"] = Relationship(back_populates="delivery")


class DeliveryLine(SQLModel, table=True):
    __tablename__ = "delivery_lines"
    __table_args__ = {"schema": "main"}

    id: str = Field(primary_key=True, index=True, default_factory=generate_cuid)
    delivery_id: str = Field(foreign_key="main.deliveries.id", nullable=False)
    item_id: str = Field(foreign_key="main.items.id", nullable=False)
    qty: float = Field(nullable=False)
    uom_id: str = Field(foreign_key="main.unit_of_measure.id", nullable=False)

    delivery: Optional[Delivery] = Relationship(back_populates="lines")
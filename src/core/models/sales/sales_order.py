from sqlmodel import SQLModel, Field, func, Relationship
from datetime import datetime
from typing import List, Optional
from src.utils import generate_cuid


class SalesOrder(SQLModel, table=True):
    __tablename__ = "sales_orders"
    __table_args__ = {"schema": "main"}

    id: str = Field(primary_key=True, index=True, default_factory=generate_cuid)
    so_number: str = Field(max_length=20, nullable=False, unique=True)
    customer_id: str = Field(foreign_key="main.customers.id", nullable=False)
    warehouse_id: str = Field(foreign_key="main.warehouses.id", nullable=False)
    status: str = Field(default="DRAFT") # DRAFT, CONFIRMED, DELIVERED, CANCELLED
    order_date: datetime = Field(default=func.now())
    modified_date: datetime = Field(
        default=func.now(), sa_column_kwargs={"onupdate": func.now()}
    )

    lines: List["SalesOrderLine"] = Relationship(back_populates="sales_order")


class SalesOrderLine(SQLModel, table=True):
    __tablename__ = "sales_order_lines"
    __table_args__ = {"schema": "main"}

    id: str = Field(primary_key=True, index=True, default_factory=generate_cuid)
    so_id: str = Field(foreign_key="main.sales_orders.id", nullable=False)
    item_id: str = Field(foreign_key="main.items.id", nullable=False)
    uom_id: str = Field(foreign_key="main.unit_of_measure.id", nullable=False)
    qty_ordered: float = Field(nullable=False)
    qty_delivered: float = Field(default=0.0)
    price: float = Field(default=0.0)

    sales_order: Optional[SalesOrder] = Relationship(back_populates="lines")
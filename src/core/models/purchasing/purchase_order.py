from sqlmodel import SQLModel, Field, func, Relationship
from datetime import datetime
from typing import List, Optional
from src.utils import generate_cuid

class PurchaseOrder(SQLModel, table=True):
    __tablename__ = "purchase_orders"
    __table_args__ = {"schema": "main"}

    id: str = Field(primary_key=True, index=True, default_factory=generate_cuid)
    po_number: str = Field(max_length=20, nullable=False, unique=True)
    supplier_id: str = Field(foreign_key="main.suppliers.id", nullable=False)
    status: str = Field(default="DRAFT") # DRAFT, APPROVED, RECEIVED, CLOSED
    order_date: datetime = Field(default=func.now())
    modified_date: datetime = Field(
        default=func.now(), sa_column_kwargs={"onupdate": func.now()}
    )

    lines: List["PurchaseOrderLine"] = Relationship(back_populates="purchase_order")


class PurchaseOrderLine(SQLModel, table=True):
    __tablename__ = "purchase_order_lines"
    __table_args__ = {"schema": "main"}

    id: str = Field(primary_key=True, index=True, default_factory=generate_cuid)
    po_id: str = Field(foreign_key="main.purchase_orders.id", nullable=False)
    item_id: str = Field(foreign_key="main.items.id", nullable=False)
    qty: float = Field(nullable=False)
    uom_id: str = Field(foreign_key="main.unit_of_measure.id", nullable=False)
    price: float = Field(default=0.0)

    purchase_order: Optional[PurchaseOrder] = Relationship(back_populates="lines")
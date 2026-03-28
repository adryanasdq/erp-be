from sqlmodel import SQLModel, Field, func, Relationship
from datetime import datetime
from typing import List, Optional
from src.utils import generate_cuid

class GoodsReceipt(SQLModel, table=True):
    __tablename__ = "goods_receipts"
    __table_args__ = {"schema": "main"}

    id: str = Field(primary_key=True, index=True, default_factory=generate_cuid)
    po_id: str = Field(foreign_key="main.purchase_orders.id", nullable=False)
    warehouse_id: str = Field(foreign_key="main.warehouses.id", nullable=False)
    received_date: datetime = Field(default=func.now())
    modified_date: datetime = Field(
        default=func.now(), sa_column_kwargs={"onupdate": func.now()}
    )

    lines: List["GoodsReceiptLine"] = Relationship(back_populates="goods_receipt")


class GoodsReceiptLine(SQLModel, table=True):
    __tablename__ = "goods_receipt_lines"
    __table_args__ = {"schema": "main"}

    id: str = Field(primary_key=True, index=True, default_factory=generate_cuid)
    receipt_id: str = Field(foreign_key="main.goods_receipts.id", nullable=False)
    item_id: str = Field(foreign_key="main.items.id", nullable=False)
    qty: float = Field(nullable=False)
    uom_id: str = Field(foreign_key="main.unit_of_measure.id", nullable=False)

    goods_receipt: Optional[GoodsReceipt] = Relationship(back_populates="lines")
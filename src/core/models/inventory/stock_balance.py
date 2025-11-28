from sqlmodel import SQLModel, Field, func
from datetime import datetime

from src.utils import generate_cuid


class StockBalance(SQLModel, table=True):
    __tablename__ = "stock_balances"
    __table_args__ = {"schema": "main"}

    id: str = Field(primary_key=True, index=True, default_factory=generate_cuid)
    item_id: str = Field(foreign_key="main.items.id", nullable=False)
    warehouse_id: str = Field(foreign_key="main.warehouses.id", nullable=False)
    qty: int = Field(nullable=False)
    qty_reserved: int = Field(nullable=False)
    qty_available: int = Field(nullable=False)
    modified_date: datetime = Field(
        default=func.now(), sa_column_kwargs={"onupdate": func.now()}
    )

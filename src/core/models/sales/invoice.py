from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class Invoice(SQLModel, table=True):
    __tablename__ = "invoices"
    
    id: Optional[str] = Field(default=None, primary_key=True)
    invoice_number: str = Field(index=True, unique=True)
    delivery_id: str = Field(foreign_key="main.deliveries.id")
    customer_id: str = Field(foreign_key="main.customers.id")
    date: datetime = Field(default_factory=datetime.now)
    total_amount: float
    status: str = Field(default="UNPAID")  # UNPAID, PAID, VOID

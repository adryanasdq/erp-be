from sqlmodel import SQLModel, Field, UniqueConstraint, func
from decimal import Decimal
from datetime import datetime

from src.utils import generate_cuid


class ItemUOMConversion(SQLModel, table=True):
    __tablename__ = "item_uom_conversions"
    __table_args__ = (
        UniqueConstraint(
            "item_id",
            "from_uom_id",
            "to_uom_id",
            name="unique_item_uom_conv",
        ),
        {"schema": "main"},
    )

    id: str = Field(primary_key=True, index=True, default_factory=generate_cuid)
    item_id: str = Field(foreign_key="main.items.id", nullable=False)
    from_uom_id: str = Field(foreign_key="main.unit_of_measure.id", nullable=False)
    to_uom_id: str = Field(foreign_key="main.unit_of_measure.id", nullable=False)
    factor: Decimal = Field(nullable=False)
    is_active: bool = Field(default=True)
    created_date: datetime = Field(default=func.now())

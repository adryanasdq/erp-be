from sqlmodel import SQLModel, Field, func
from datetime import datetime

from src.utils import generate_cuid


class Item(SQLModel, table=True):
    __tablename__ = "items"
    __table_args__ = {"schema": "main"}

    id: str = Field(primary_key=True, index=True, default_factory=generate_cuid)
    code: str = Field(max_length=15, nullable=False, unique=True)
    name: str = Field(max_length=50, nullable=False)
    category: str | None = Field(default=None)
    uom_id: str = Field(foreign_key="main.unit_of_measure.id", nullable=False)
    is_hidden: bool = Field(default=False)
    modified_date: datetime = Field(
        default=func.now(), sa_column_kwargs={"onupdate": func.now()}
    )

from sqlmodel import SQLModel, Field, func
from datetime import datetime

from src.utils import generate_cuid


class Warehouse(SQLModel, table=True):
    __tablename__ = "warehouses"
    __table_args__ = {"schema": "main"}

    id: str = Field(primary_key=True, index=True, default_factory=generate_cuid)
    name: str = Field(max_length=50, nullable=False)
    location: str | None = Field(default=None, max_length=255)
    modified_date: datetime = Field(
        default=func.now(), sa_column_kwargs={"onupdate": func.now()}
    )

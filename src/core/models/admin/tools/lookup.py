from sqlmodel import SQLModel, Field, func
from typing import Optional
from datetime import datetime

from src.utils import generate_cuid


class Lookup(SQLModel, table=True):
    __tablename__ = "lookup"
    __table_args__ = {"schema": "admin"}

    id: Optional[str] = Field(primary_key=True, default_factory=generate_cuid)
    group_code: str = Field(max_length=100, nullable=False)
    group_desc: str = Field(nullable=True)
    value: str = Field(max_length=100, nullable=False)  #Immutable
    label: str = Field(max_length=225)
    order_index: int = Field(default=0)
    is_hidden: bool = Field(default=False)
    modified_date: datetime = Field(
        default=func.now(), sa_column_kwargs={"onupdate": func.now()}
    )

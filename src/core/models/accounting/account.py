from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship, func

from src.utils import generate_cuid


class Account(SQLModel, table=True):
    __tablename__ = "accounts"
    __table_args__ = {"schema": "main"}

    id: Optional[str] = Field(primary_key=True, default_factory=generate_cuid)
    code: str = Field(index=True, unique=True)
    name: str
    type: str  # ASSET, LIABILITY, EQUITY, REVENUE, EXPENSE
    active: bool = Field(default=True)
    modified_date: datetime = Field(
        default=func.now(), sa_column_kwargs={"onupdate": func.now()}
    )

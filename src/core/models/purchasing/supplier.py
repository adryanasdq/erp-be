from sqlmodel import SQLModel, Field, func
from datetime import datetime
from src.utils import generate_cuid

class Supplier(SQLModel, table=True):
    __tablename__ = "suppliers"
    __table_args__ = {"schema": "main"}

    id: str = Field(primary_key=True, index=True, default_factory=generate_cuid)
    code: str = Field(max_length=15, nullable=False, unique=True)
    name: str = Field(max_length=100, nullable=False)
    status: str = Field(default="ACTIVE") # ACTIVE, INACTIVE
    modified_date: datetime = Field(
        default=func.now(), sa_column_kwargs={"onupdate": func.now()}
    )
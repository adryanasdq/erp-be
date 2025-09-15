from sqlmodel import SQLModel, Field, func
from datetime import date

from src.utils import generate_cuid

class Department(SQLModel, table=True):
    __tablename__ = "departments"
    __table_args__ = {"schema": "main"}
    
    id: str = Field(default_factory=generate_cuid, primary_key=True, index=True)
    name: str = Field(max_length=50, nullable=False)
    description: str | None = Field(default=None, max_length=255)
    modified_date: date = Field(
        default=func.now(),
        sa_column_kwargs={"onupdate": func.now()}
    )
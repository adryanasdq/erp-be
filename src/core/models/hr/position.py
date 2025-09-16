from sqlmodel import SQLModel, Field, func, Relationship
from datetime import datetime

from src.core.models.hr.department import Department


class Position(SQLModel, table=True):
    __tablename__ = "positions"
    __table_args__ = {"schema": "main"}

    id: str = Field(primary_key=True, index=True)
    title: str = Field(max_length=50, nullable=False)
    description: str | None = Field(max_length=255, nullable=True)
    department_id: str = Field(
        foreign_key="main.departments.id", ondelete="CASCADE", nullable=False
    )
    modified_date: datetime = Field(
        default=func.now(), sa_column_kwargs={"onupdate": func.now()}
    )

    # Relationships
    dept: "Department" = Relationship(back_populates="positions")

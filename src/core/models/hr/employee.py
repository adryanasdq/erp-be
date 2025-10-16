from sqlmodel import Relationship, SQLModel, Field, func
from datetime import date, datetime

from src.core.models.hr.position import Position


class Employee(SQLModel, table=True):
    __tablename__ = "employees"
    __table_args__ = {"schema": "main"}

    id: str = Field(primary_key=True, index=True)
    name: str = Field(max_length=50, nullable=False)
    position_id: str = Field(
        foreign_key="main.positions.id", ondelete="CASCADE", nullable=False
    )
    manager_id: str = Field(nullable=True)
    hire_date: date = Field(default=func.now())
    status: str = Field(default="Active", max_length=20)
    modified_date: datetime = Field(
        default=func.now(), sa_column_kwargs={"onupdate": func.now()}
    )

    # Relationships
    position: "Position" = Relationship(back_populates="employees")

from sqlmodel import SQLModel, Field, func, Relationship
from datetime import datetime


class Department(SQLModel, table=True):
    __tablename__ = "departments"
    __table_args__ = {"schema": "main"}
    
    id: str = Field(primary_key=True, index=True)
    name: str = Field(max_length=50, nullable=False)
    description: str | None = Field(default=None, max_length=255)
    modified_date: datetime = Field(
        default=func.now(),
        sa_column_kwargs={"onupdate": func.now()}
    )

    # Relationships
    positions: list["Position"] = Relationship(back_populates="dept", cascade_delete=True)
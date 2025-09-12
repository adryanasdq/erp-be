from sqlmodel import SQLModel, Field, func

from src.utils import generate_cuid

class Employee(SQLModel, table=True):
    __tablename__ = 'employees'
    __table_args__ = {'schema': 'main'}

    id: str = Field(default_factory=generate_cuid, primary_key=True, index=True)
    name: str = Field(max_length=50, nullable=False)
    position_id: str = Field(nullable=False, max_length=50)
    department_id: str = Field(nullable=False, max_length=50)
    hire_date: str = Field(default=func.now())
    status: str = Field(default="active", max_length=20)
    modified_date: str = Field(
        default=func.now(),
        sa_column_kwargs={"onupdate": func.now()}
    )
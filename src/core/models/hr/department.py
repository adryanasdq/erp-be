from sqlmodel import SQLModel, Field

from src.utils import generate_cuid

class Department(SQLModel, table=True):
    __tablename__ = "departments"
    __table_args__ = {"schema": "main"}
    
    id: str = Field(default_factory=generate_cuid, primary_key=True, index=True)
    name: str = Field(max_length=50, nullable=False)
    description: str | None = Field(default=None, max_length=255)
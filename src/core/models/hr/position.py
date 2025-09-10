from sqlmodel import SQLModel, Field

from src.utils import generate_cuid

class Position(SQLModel, table=True):
    __tablename__ = 'positions'
    __table_args__ = {'schema': 'main'}
    
    id: str = Field(default_factory=generate_cuid, primary_key=True, index=True)
    title: str = Field(max_length=50, nullable=False)
    description: str | None = Field(max_length=255, nullable=True)
    reports_to_pos_id: str | None = Field(nullable=True, max_length=50)
from sqlmodel import Relationship, SQLModel, Field, func
from typing import List, Optional
from datetime import datetime


class Menu(SQLModel, table=True):
    __tablename__ = "menu"
    __table_args__ = {"schema": "admin"}

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=100, nullable=False)
    url: str = Field(max_length=200, nullable=False)
    icon: Optional[str] = Field(default=None, max_length=100)
    parent_id: Optional[int] = Field(
        default=None, foreign_key="admin.menu.id", nullable=True
    )
    order_index: int = Field(default=0)
    is_hidden: bool = Field(default=False)
    modified_date: datetime = Field(
        default=func.now(), sa_column_kwargs={"onupdate": func.now()}
    )

    # Relationships
    children: List["Menu"] = Relationship(
        back_populates="parent",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    parent: Optional["Menu"] = Relationship(
        back_populates="children", sa_relationship_kwargs={"remote_side": "Menu.id"}
    )

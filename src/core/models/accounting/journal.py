from datetime import datetime
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship, func
from src.utils import generate_cuid


class JournalEntry(SQLModel, table=True):
    __tablename__ = "journal_entries"
    __table_args__ = {"schema": "main"}

    id: str = Field(primary_key=True, index=True, default_factory=generate_cuid)
    date: datetime = Field(default_factory=datetime.now)
    reference_type: str  # e.g., "MANUAL", "INVOICE", "GRN"
    reference_id: Optional[str] = None
    description: Optional[str] = None
    modified_date: datetime = Field(
        default=func.now(), sa_column_kwargs={"onupdate": func.now()}
    )

    lines: List["JournalEntryLine"] = Relationship(back_populates="journal_entry")


class JournalEntryLine(SQLModel, table=True):
    __tablename__ = "journal_entry_lines"
    __table_args__ = {"schema": "main"}

    id: str = Field(primary_key=True, index=True, default_factory=generate_cuid)
    journal_entry_id: str = Field(foreign_key="main.journal_entries.id")
    account_id: str = Field(foreign_key="main.accounts.id")
    debit: float = Field(default=0.0)
    credit: float = Field(default=0.0)

    journal_entry: "JournalEntry" = Relationship(back_populates="lines")

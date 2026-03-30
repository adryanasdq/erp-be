from datetime import datetime
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from .account import Account


class JournalEntry(SQLModel, table=True):
    __tablename__ = "journal_entries"
    id: Optional[str] = Field(default=None, primary_key=True)
    date: datetime = Field(default_factory=datetime.now)
    reference_type: str
    reference_id: str
    description: Optional[str] = None

    lines: List["JournalEntryLine"] = Relationship(back_populates="journal_entry")


class JournalEntryLine(SQLModel, table=True):
    __tablename__ = "journal_entry_lines"
    id: Optional[str] = Field(default=None, primary_key=True)
    journal_entry_id: str = Field(foreign_key="journal_entries.id")
    account_id: str = Field(foreign_key="accounts.id")
    debit: float = Field(default=0.0)
    credit: float = Field(default=0.0)

    journal_entry: JournalEntry = Relationship(back_populates="lines")

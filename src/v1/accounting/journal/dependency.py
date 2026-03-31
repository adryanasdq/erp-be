from fastapi import Depends
from sqlmodel import Session as SessionType, select

from src.core.models.accounting.journal import JournalEntry as DbJournal
from src.core.settings.database import get_session

from .exception import JournalUnbalanced, JournalEntryNotFound


def get_journal_by_id(id: str, session: SessionType = Depends(get_session)):
    db_journal = session.get(DbJournal, id)
    if not db_journal:
        raise JournalEntryNotFound()
    return db_journal


def validate_journal_entry(data: DbJournal, session: SessionType, id: str = None):
    # 1. Enforcement: Total Debit must equal Total Credit
    total_debit = sum(line.debit for line in data.lines)
    total_credit = sum(line.credit for line in data.lines)

    if abs(total_debit - total_credit) > 0.0001:
        raise JournalUnbalanced()

    if not id:
        # Create Logic
        db_journal = DbJournal(
            **data.model_dump(exclude_unset=True, exclude={"id", "lines"})
        )
        # Re-attach lines (SQLModel handles the relationship)
        db_journal.lines = data.lines
    else:
        # Update Logic (following your Supplier Pattern)
        db_journal = get_journal_by_id(id, session)
        for key, attr in data.model_dump(exclude_unset=True, exclude={"lines"}).items():
            setattr(db_journal, key, attr)

    return db_journal

from sqlmodel import Session as SessionType, select
from src.core.models.accounting.journal import (
    JournalEntry as DbJournal,
    JournalEntryLine as DbLine,
    Account as DbAccount,
)
from src.core.schemas.accounting.journal import JournalEntrySchema
from .exception import JournalUnbalanced, AccountNotFound


def validate_journal_entry(data: JournalEntrySchema, session: SessionType):
    # 1. Accounting Rule: Debit == Credit
    total_debit = sum(line.debit for line in data.lines)
    total_credit = sum(line.credit for line in data.lines)

    if abs(total_debit - total_credit) > 0.001:  # Handle float precision
        raise JournalUnbalanced()

    # 2. Prepare DB Objects
    db_entry = DbJournal(**data.model_dump(exclude={"lines"}))
    db_entry.lines = [DbLine(**line.model_dump()) for line in data.lines]

    return db_entry


def get_account_by_code(code: str, session: SessionType):
    account = session.exec(select(DbAccount).where(DbAccount.code == code)).first()
    if not account:
        raise AccountNotFound(code)
    return account

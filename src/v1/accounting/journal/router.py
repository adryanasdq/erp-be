from fastapi import APIRouter, Depends
from sqlmodel import Session as SessionType
from src.core.schemas.accounting.journal import JournalEntrySchema
from src.core.settings.database import get_session
from .dependency import validate_journal_entry
from .service import commit_journal_entry

router = APIRouter(prefix="/accounting/journals", tags=["Accounting"])


@router.post("/")
def create_manual_journal(
    data: JournalEntrySchema, session: SessionType = Depends(get_session)
):
    """Used for manual adjustments by accountants."""
    db_entry = validate_journal_entry(data, session)
    return commit_journal_entry(db_entry, session)

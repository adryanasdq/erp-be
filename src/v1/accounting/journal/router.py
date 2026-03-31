from fastapi import APIRouter, Depends
from sqlmodel import Session as SessionType
from src.core.settings.database import get_session
from src.core.models.accounting.journal import JournalEntry
from .dependency import validate_journal_entry, get_journal_by_id
from .service import create, delete

router = APIRouter(prefix="/accounting/journals", tags=["Journals"])


@router.post("/")
def create_journal(data: JournalEntry, session: SessionType = Depends(get_session)):
    validated_data = validate_journal_entry(data, session)
    return create(validated_data, session)


@router.delete("/{id}", response_model=None)
def delete_journal(
    data: JournalEntry = Depends(get_journal_by_id),
    session: SessionType = Depends(get_session),
):
    return delete(data, session)

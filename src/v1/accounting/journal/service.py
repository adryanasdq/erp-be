from fastapi import HTTPException
from sqlmodel import Session as SessionType
from src.core.models.accounting.journal import JournalEntry


def create(journal: JournalEntry, session: SessionType):
    try:
        session.add(journal)
        session.commit()
        session.refresh(journal)
        return journal
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def delete(journal: JournalEntry, session: SessionType):
    try:
        session.delete(journal)
        session.commit()
        return {"message": f"Journal Entry {journal.id} deleted successfully"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))

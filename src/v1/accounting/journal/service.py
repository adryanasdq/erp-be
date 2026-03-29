from sqlmodel import Session as SessionType


def commit_journal_entry(db_entry, session: SessionType):
    try:
        session.add(db_entry)
        session.commit()
        session.refresh(db_entry)
        return db_entry
    except Exception as e:
        session.rollback()
        raise e

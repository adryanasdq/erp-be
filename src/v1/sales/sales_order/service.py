from fastapi import HTTPException
from sqlmodel import Session as SessionType, select
from src.core.models.sales.sales_order import SalesOrder as DbSO


def get_all(session: SessionType):
    stmnt = select(DbSO)

    result = session.exec(stmnt)
    return result.all()


def commit_so_transaction(db_so: DbSO, session: SessionType):
    try:
        session.add(db_so)
        session.commit()
        session.refresh(db_so)
        return db_so
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))

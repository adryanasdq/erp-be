from fastapi import HTTPException
from sqlmodel import select
from sqlmodel import Session as SessionType

from src.core.models.admin.tools.lookup import Lookup as DbLookup
from src.core.schemas.admin.tools.lookup import Lookup


def get_group(session: SessionType):
    stmnt = select(DbLookup.group_code, DbLookup.group_desc).distinct()

    query = session.exec(stmnt)
    results = query.all()

    return {
        "data": [
            {
                "group_code": row[0],
                "group_desc": row[1],
            }
            for row in results
        ],
        "total": len(results),
    }


def get_group_options(group_code: str, session: SessionType):
    stmnt = select(DbLookup).where(DbLookup.group_code == group_code)

    result = session.exec(stmnt)
    return result.all()


def get_all(session: SessionType):
    stmnt = select(DbLookup)

    result = session.exec(stmnt)
    return result.all()


def create(option: DbLookup, session: SessionType):
    try:
        session.add(option)
        session.commit()
        session.refresh(option)
        return Lookup.model_validate(option)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def update(option: DbLookup, session: SessionType):
    try:
        session.commit()
        session.refresh(option)
        return Lookup.model_validate(option)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def delete(option: DbLookup, session: SessionType):
    try:
        session.delete(option)
        session.commit()
        return {"message": f"Option with id {option.id} deleted successfully"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))

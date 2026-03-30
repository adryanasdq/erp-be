from sqlmodel import Session as SessionType
from fastapi import HTTPException
from sqlmodel import Session as SessionType
from src.core.models.accounting.account import Account


def commit_account_db(db_account, session: SessionType):
    try:
        session.add(db_account)
        session.commit()
        session.refresh(db_account)
        return db_account
    except Exception as e:
        session.rollback()
        raise e


def update(account: Account, session: SessionType):
    try:
        session.commit()
        session.refresh(account)
        return Account.model_validate(account)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def delete(account: Account, session: SessionType):
    try:
        session.delete(account)
        session.commit()
        return {"message": f"Account with id {account.id} deleted successfully"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))

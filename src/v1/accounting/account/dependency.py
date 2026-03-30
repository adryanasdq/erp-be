from datetime import datetime

from fastapi import Depends
from sqlmodel import Session as SessionType, select
from src.core.models.accounting.account import Account as DbAccount
from src.core.settings.database import get_session

from .exception import AccountNotFound, AccountCodeExists


def get_account_by_id(id: str, session: SessionType = Depends(get_session)):
    acc = session.get(DbAccount, id)
    if not acc:
        raise AccountNotFound()
    return acc


def validate_account(account: DbAccount, session: SessionType, id: str = None):
    if not id:
        existing = session.exec(
            select(DbAccount).where(DbAccount.code == account.code)
        ).first()
        if existing:
            raise AccountCodeExists()

        db_account = DbAccount(**account.model_dump(exclude_unset=True, exclude={"id"}))
    else:
        db_account = get_account_by_id(id, session)
        for key, attr in account.model_dump(exclude_unset=True).items():
            setattr(db_account, key, attr)

    db_account.modified_date = datetime.now()
    return db_account


def get_all_accounts(session: SessionType, acc_type: str = None):
    statement = select(DbAccount)
    if acc_type:
        statement = statement.where(DbAccount.type == acc_type)
    return session.exec(statement).all()


def get_account_by_code(code: str, session: SessionType):
    acc = session.exec(select(DbAccount).where(DbAccount.code == code)).first()
    if not acc:
        raise AccountNotFound()
    return acc

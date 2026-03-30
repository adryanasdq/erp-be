from fastapi import APIRouter, Depends, Query
from sqlmodel import Session as SessionType

from src.core.settings.database import get_session
from src.core.schemas.accounting.account import AccountSchema

from .dependency import (
    get_account_by_id,
    get_all_accounts,
    validate_account,
)
from .service import commit_account_db, delete, update


router = APIRouter(prefix="/accounts", tags=["Accounts"])


@router.post("/")
def create_account(data: AccountSchema, session: SessionType = Depends(get_session)):
    db_acc = validate_account(data, session)
    return commit_account_db(db_acc, session)


@router.get("/")
def list_accounts(type: str = Query(None), session: SessionType = Depends(get_session)):
    return get_all_accounts(session, type)


@router.put("/{id}")
def update_account(
    id: str, data: AccountSchema, session: SessionType = Depends(get_session)
):
    validated_account = validate_account(data, session, id)
    return update(validated_account, session)


@router.delete("/{id}")
def delete_account(
    data: AccountSchema = Depends(get_account_by_id),
    session: SessionType = Depends(get_session),
):
    return delete(data, session)

from datetime import datetime
from fastapi import Depends
from sqlmodel import select, Session as SessionType

from src.core.models.admin.tools.lookup import Lookup as DbLookup
from src.core.schemas.admin.tools.lookup import Lookup
from src.core.settings.database import get_session

from .exception import GroupCodeNotFound, OptionAlreadyExists, OptionNotFound


def get_group_code(group_code: str, session: SessionType):
    stmnt = select(DbLookup).where(DbLookup.group_code == group_code)
    query = session.exec(stmnt)
    db_group_code = query.first()

    if not db_group_code:
        raise GroupCodeNotFound()
    return db_group_code


def check_if_option_exists(group_code: str, value: str, session: SessionType):
    stmnt = select(DbLookup).where(
        DbLookup.group_code == group_code, DbLookup.value == value
    )

    query = session.exec(stmnt)
    db_lookup = query.first()

    if db_lookup:
        raise OptionAlreadyExists(value)
    return


def get_option_by_id(id: str, session: SessionType = Depends(get_session)):
    db_option = session.get(DbLookup, id)

    if not db_option:
        raise OptionNotFound()
    return db_option


def validate_option(option: Lookup, session: SessionType, id: str = None):
    get_group_code(option.group_code, session)

    if not id:
        check_if_option_exists(option.group_code, option.value, session)
        db_option = DbLookup(**option.model_dump(exclude_unset=True, exclude={"id"}))
    else:
        db_option = get_option_by_id(id, session)
        for key, attr in option.model_dump(
            exclude_unset=True, exclude={"id", "value"}
        ).items():
            setattr(db_option, key, attr)

    db_option.modified_date = datetime.now()
    return db_option

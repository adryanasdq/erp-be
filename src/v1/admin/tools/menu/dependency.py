from datetime import datetime
from fastapi import Depends
from sqlmodel import Session as SessionType

from src.core.settings.database import get_session
from src.core.models.admin.tools.menu import Menu as DbMenu
from src.core.schemas.admin.tools.menu import Menu

from .exception import MenuNotFound


def get_menu_by_id(
    id: str, session: SessionType = Depends(get_session)
):
    db_menu = session.get(DbMenu, id)
    if not db_menu:
        raise MenuNotFound()
    return db_menu


def validate_menu(menu: Menu, session: SessionType, id: str = None):
    if id is None:
        db_menu = DbMenu(
            id=menu.id, **menu.model_dump(exclude_unset=True, exclude={"id"})
        )
    else:
        db_menu = get_menu_by_id(id, session)
        for key, attr in menu.model_dump(exclude_unset=True).items():
            setattr(db_menu, key, attr)

    db_menu.modified_date = datetime.now()
    return db_menu
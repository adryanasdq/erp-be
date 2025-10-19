from datetime import datetime
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.settings.database import get_session
from src.core.models.admin.tools.menu import Menu as DbMenu
from src.core.schemas.admin.tools.menu import Menu

from .exception import MenuNotFound


async def get_menu_by_id(
    id: int, session: AsyncSession = Depends(get_session)
):
    db_menu = await session.get(DbMenu, id)
    if not db_menu:
        raise MenuNotFound()
    return db_menu


async def validate_menu(menu: Menu, session: AsyncSession, id: int = None):
    if id is None:
        db_menu = DbMenu(
            id=menu.id, **menu.model_dump(exclude_unset=True, exclude={"id"})
        )
    else:
        db_menu = await get_menu_by_id(id, session)
        for key, attr in menu.model_dump(exclude_unset=True).items():
            setattr(db_menu, key, attr)

    db_menu.modified_date = datetime.now()
    return db_menu
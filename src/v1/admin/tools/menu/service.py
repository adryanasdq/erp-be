from fastapi import HTTPException
from sqlmodel import select
from sqlalchemy.orm import Session as SessionType

from src.core.models.admin.tools.menu import Menu as DbMenu
from src.core.schemas.admin.tools.menu import Menu


def get_all(session: SessionType):
    stmnt = select(DbMenu)

    result = session.execute(stmnt)
    return result.scalars().all()


def get_by_id(menu_id: str, session: SessionType):
    stmnt = select(DbMenu).where(DbMenu.id == menu_id)

    result = session.execute(stmnt)
    return result.scalar_one_or_none()


def create(menu: DbMenu, session: SessionType):
    try:
        session.add(menu)
        session.commit()
        session.refresh(menu)
        return Menu.model_validate(menu)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def update(menu: DbMenu, session: SessionType):
    try:
        session.commit()
        session.refresh(menu)
        return Menu.model_validate(menu)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def delete(menu: DbMenu, session: SessionType):
    try:
        session.delete(menu)
        session.commit()
        return {"message": f"Menu with id {menu.id} deleted successfully"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))

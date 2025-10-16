from fastapi import HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.models.admin.tools.menu import Menu as DbMenu
from src.core.schemas.admin.tools.menu import Menu


async def get_all(session: AsyncSession):
    stmnt = select(DbMenu)

    result = await session.exec(stmnt)
    return result.all()


async def get_by_id(menu_id: str, session: AsyncSession):
    stmnt = select(DbMenu).where(DbMenu.id == menu_id)

    result = await session.exec(stmnt)
    return result.first()


async def create(menu: DbMenu, session: AsyncSession):
    try:
        session.add(menu)
        await session.commit()
        await session.refresh(menu)
        return Menu.model_validate(menu)
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    

async def update(menu: DbMenu, session: AsyncSession):
    try:
        await session.commit()
        await session.refresh(menu)
        return Menu.model_validate(menu)
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    

async def delete(menu: DbMenu, session: AsyncSession):
    try:
        await session.delete(menu)
        await session.commit()
        return {"message": f"Menu with id {menu.id} deleted successfully"}
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
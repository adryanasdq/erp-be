from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.schemas.admin.tools.menu import Menu
from src.core.settings.database import get_session

from .dependency import get_menu_by_id, validate_menu
from .service import get_all, get_by_id, create, update, delete


router = APIRouter(prefix="/menus", tags=["Menus"])


@router.get("/")
async def get_all_menus(session: AsyncSession = Depends(get_session)):
    menus = await get_all(session)
    return menus


@router.get("/{id}")
async def get_menu(id: str, session: AsyncSession = Depends(get_session)):
    menu = await get_by_id(id, session)
    return menu


@router.post("/")
async def create_menu(data: Menu, session: AsyncSession = Depends(get_session)):
    validated_menu = await validate_menu(data, session)
    return await create(validated_menu, session)


@router.put("/{id}")
async def update_menu(
    id: str, data: Menu, session: AsyncSession = Depends(get_session)
):
    validated_menu = await validate_menu(data, session, id)
    return await update(validated_menu, session)


@router.delete("/{id}")
async def delete_menu(
    data: Menu = Depends(get_menu_by_id),
    session: AsyncSession = Depends(get_session),
):
    return await delete(data, session)
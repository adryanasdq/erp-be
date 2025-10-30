from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as SessionType

from src.core.schemas.admin.tools.menu import Menu
from src.core.settings.database import get_session

from .dependency import get_menu_by_id, validate_menu
from .service import get_all, get_by_id, create, update, delete


router = APIRouter(prefix="/menus", tags=["Menus"])


@router.get("/")
def get_all_menus(session: SessionType = Depends(get_session)):
    menus = get_all(session)
    return menus


@router.get("/{id}")
def get_menu(id: str, session: SessionType = Depends(get_session)):
    menu = get_by_id(id, session)
    return menu


@router.post("/")
def create_menu(data: Menu, session: SessionType = Depends(get_session)):
    validated_menu = validate_menu(data, session)
    return create(validated_menu, session)


@router.put("/{id}")
def update_menu(
    id: str, data: Menu, session: SessionType = Depends(get_session)
):
    validated_menu = validate_menu(data, session, id)
    return update(validated_menu, session)


@router.delete("/{id}")
def delete_menu(
    data: Menu = Depends(get_menu_by_id),
    session: SessionType = Depends(get_session),
):
    return delete(data, session)
from fastapi import APIRouter, Depends
from sqlmodel import Session as SessionType

from src.core.schemas.admin.tools.lookup import Lookup
from src.core.settings.database import get_session

from .dependency import get_option_by_id, validate_option
from .service import get_group, get_group_options, get_all, create, update, delete


router = APIRouter(prefix="/lookup", tags=["Lookup"])


@router.get("/group")
def get_all_group_code(session: SessionType = Depends(get_session)):
    groups = get_group(session)
    return groups


@router.get("/{group_code}")
def get_all_group_options(group_code: str, session: SessionType = Depends(get_session)):
    options = get_group_options(group_code, session)
    return options


@router.get("/")
def get_all_options(session: SessionType = Depends(get_session)):
    options = get_all(session)
    return options


@router.post("/")
def create_option(data: Lookup, session: SessionType = Depends(get_session)):
    validated_option = validate_option(data, session)
    return create(validated_option, session)


@router.put("/{id}")
def update_option(
    id: str, data: Lookup, session: SessionType = Depends(get_session)
):
    validated_option = validate_option(data, session, id)
    return update(validated_option, session)


@router.delete("/{id}")
def delete_option(
    data: Lookup = Depends(get_option_by_id),
    session: SessionType = Depends(get_session),
):
    return delete(data, session)

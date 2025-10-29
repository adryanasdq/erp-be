from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.schemas.admin.tools.lookup import Lookup
from src.core.settings.database import get_session

from .dependency import get_option_by_id, validate_option
from .service import get_group, get_group_options, get_all, create, update, delete


router = APIRouter(prefix="/lookup", tags=["Lookup"])


@router.get("/group")
async def get_all_group_code(session: AsyncSession = Depends(get_session)):
    groups = await get_group(session)
    return groups


@router.get("/{group_code}")
async def get_all_group_options(group_code: str, session: AsyncSession = Depends(get_session)):
    options = await get_group_options(group_code, session)
    return options


@router.get("/")
async def get_all_options(session: AsyncSession = Depends(get_session)):
    options = await get_all(session)
    return options


@router.post("/")
async def create_option(data: Lookup, session: AsyncSession = Depends(get_session)):
    validated_option = await validate_option(data, session)
    return await create(validated_option, session)


@router.put("/{id}")
async def update_option(
    id: str, data: Lookup, session: AsyncSession = Depends(get_session)
):
    validated_option = await validate_option(data, session, id)
    return await update(validated_option, session)


@router.delete("/{id}")
async def delete_option(
    data: Lookup = Depends(get_option_by_id),
    session: AsyncSession = Depends(get_session),
):
    return await delete(data, session)

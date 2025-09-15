from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.schemas.hr.position import Position
from src.core.settings.database import get_session

from .dependency import get_position_by_id, validate_position
from .service import get_all, get_by_id, create, update, delete


router = APIRouter(prefix="/positions", tags=["Positions"])


@router.get("/")
async def get_all_positions(session: AsyncSession = Depends(get_session)):
    positions = await get_all(session)
    return positions


@router.get("/{id}")
async def get_position(id: str, session: AsyncSession = Depends(get_session)):
    position = await get_by_id(id, session)
    return position


@router.post("/")
async def create_position(data: Position, session: AsyncSession = Depends(get_session)):
    validated_position = await validate_position(data, session)
    return await create(validated_position, session)


@router.put("/{id}")
async def update_position(
    id: str, data: Position, session: AsyncSession = Depends(get_session)
):
    validated_position = await validate_position(data, session, id)
    return await update(validated_position, session)


@router.delete("/{id}")
async def delete_position(
    data: Position = Depends(get_position_by_id),
    session: AsyncSession = Depends(get_session),
):
    return await delete(data, session)

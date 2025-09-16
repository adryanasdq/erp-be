from datetime import datetime
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.settings.database import get_session
from src.core.models.hr.position import Position as DbPosition
from src.core.schemas.hr.position import Position
from src.utils import generate_custom_id
from src.v1.hr.department.dependency import get_department_by_id

from .exception import PositionIdExists, PositionNotFound


async def check_if_position_exists(pos_id: str, session: AsyncSession):
    db_pos = await session.get(DbPosition, pos_id)
    if db_pos:
        raise PositionIdExists()
    return


async def get_position_by_id(
    pos_id: str, session: AsyncSession = Depends(get_session)
):
    db_pos = await session.get(DbPosition, pos_id)
    if not db_pos:
        raise PositionNotFound()
    return db_pos


async def validate_position(pos: Position, session: AsyncSession, id: str = None):
    await get_department_by_id(pos.department_id, session)

    if id is None:
        pos.id = await generate_custom_id("pos", session)
        await check_if_position_exists(pos.id, session)
        db_pos = DbPosition(
            id=pos.id, **pos.model_dump(exclude_unset=True, exclude={"id"})
        )
    else:
        db_pos = await get_position_by_id(id, session)
        for key, attr in pos.model_dump(exclude_unset=True).items():
            setattr(db_pos, key, attr)

    db_pos.modified_date = datetime.now()
    return db_pos
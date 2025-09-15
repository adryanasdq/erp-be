from fastapi import HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.models.hr.position import Position as DbPosition
from src.core.schemas.hr.position import Position


async def get_all(session: AsyncSession):
    stmnt = select(DbPosition)

    result = await session.exec(stmnt)
    return result.all()


async def get_by_id(position_id: str, session: AsyncSession):
    stmnt = select(DbPosition).where(DbPosition.id == position_id)

    result = await session.exec(stmnt)
    return result.first()


async def create(position: DbPosition, session: AsyncSession):
    try:
        session.add(position)
        await session.commit()
        await session.refresh(position)
        return Position.model_validate(position)
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


async def update(position: DbPosition, session: AsyncSession):
    try:
        await session.commit()
        await session.refresh(position)
        return Position.model_validate(position)
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    

async def delete(position: DbPosition, session: AsyncSession):
    try:
        await session.delete(position)
        await session.commit()
        return {"message": f"Position with id {position.id} deleted successfully"}
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
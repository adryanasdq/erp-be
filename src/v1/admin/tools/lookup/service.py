from fastapi import HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import load_only

from src.core.models.admin.tools.lookup import Lookup as DbLookup
from src.core.schemas.admin.tools.lookup import Lookup


async def get_group(session: AsyncSession):
    stmnt = select(DbLookup.group_code, DbLookup.group_desc).distinct()

    query = await session.exec(stmnt)
    results = query.all()

    # TODO:
    # Change to model_validate and model_dump when this is not async anymore
    # Async seems to be overkill for this project
    return {"data": [{"group_code": r[0], "group_desc": r[1]} for r in results]}


async def get_group_options(group_code: str, session: AsyncSession):
    stmnt = select(DbLookup).where(DbLookup.group_code == group_code)

    result = await session.exec(stmnt)
    return result.all()


async def get_all(session: AsyncSession):
    stmnt = select(DbLookup)

    result = await session.exec(stmnt)
    return result.all()


async def create(option: DbLookup, session: AsyncSession):
    try:
        session.add(option)
        await session.commit()
        await session.refresh(option)
        return Lookup.model_validate(option)
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


async def update(option: DbLookup, session: AsyncSession):
    try:
        await session.commit()
        await session.refresh(option)
        return Lookup.model_validate(option)
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


async def delete(option: DbLookup, session: AsyncSession):
    try:
        await session.delete(option)
        await session.commit()
        return {"message": f"Option with id {option.id} deleted successfully"}
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))

from fastapi import HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.models.hr.department import Department as DbDepartment
from src.core.schemas.hr.department import Department


async def get_all(session: AsyncSession):
    stmnt = select(DbDepartment)

    result = await session.exec(stmnt)
    return result.all()


async def get_by_id(department_id: str, session: AsyncSession):
    stmnt = select(DbDepartment).where(DbDepartment.id == department_id)

    result = await session.exec(stmnt)
    return result.first()


async def create(department: DbDepartment, session: AsyncSession):
    try:
        session.add(department)
        await session.commit()
        await session.refresh(department)
        return Department.model_validate(department)
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


async def update(department: DbDepartment, session: AsyncSession):
    try:
        await session.commit()
        await session.refresh(department)
        return Department.model_validate(department)
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    

async def delete(department: DbDepartment, session: AsyncSession):
    try:
        await session.delete(department)
        await session.commit()
        return {"message": f"Department with id {department.id} deleted successfully"}
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
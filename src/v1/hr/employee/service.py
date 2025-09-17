from fastapi import HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.models.hr.employee import Employee as DbEmployee
from src.core.schemas.hr.employee import Employee


async def get_all(session: AsyncSession):
    stmnt = select(DbEmployee)

    result = await session.exec(stmnt)
    return result.all()


async def get_by_id(employee_id: str, session: AsyncSession):
    stmnt = select(DbEmployee).where(DbEmployee.id == employee_id)

    result = await session.exec(stmnt)
    return result.first()


async def create(employee: DbEmployee, session: AsyncSession):
    try:
        session.add(employee)
        await session.commit()
        await session.refresh(employee)
        return Employee.model_validate(employee)
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    

async def update(employee: DbEmployee, session: AsyncSession):
    try:
        await session.commit()
        await session.refresh(employee)
        return Employee.model_validate(employee)
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    

async def delete(employee: DbEmployee, session: AsyncSession):
    try:
        await session.delete(employee)
        await session.commit()
        return {"message": f"Employee with id {employee.id} deleted successfully"}
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
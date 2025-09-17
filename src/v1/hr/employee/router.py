from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models.hr.employee import Employee
from src.core.schemas.hr.employee import Employee
from src.core.settings.database import get_session

from .dependency import get_employee_by_id, validate_employee
from .service import get_all, get_by_id, create, update, delete


router = APIRouter(prefix="/employees", tags=["Employees"])


@router.get("/")
async def get_all_employees(session: AsyncSession = Depends(get_session)):
    employees = await get_all(session)
    return employees


@router.get("/{id}")
async def get_employee(id: str, session: AsyncSession = Depends(get_session)):
    employee = await get_by_id(id, session)
    return employee


@router.post("/")
async def create_employee(data: Employee, session: AsyncSession = Depends(get_session)):
    validated_employee = await validate_employee(data, session)
    return await create(validated_employee, session)


@router.put("/{id}")
async def update_employee(
    id: str, data: Employee, session: AsyncSession = Depends(get_session)
):
    validated_employee = await validate_employee(data, session, id)
    return await update(validated_employee, session)


@router.delete("/{id}")
async def delete_employee(
    data: Employee = Depends(get_employee_by_id),
    session: AsyncSession = Depends(get_session),
):
    return await delete(data, session)
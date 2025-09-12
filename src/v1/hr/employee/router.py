from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.settings.database import get_session
from .service import EmployeeService


router = APIRouter(prefix="/employees", tags=["Employees"])

@router.get("/")
async def get_employees(session: AsyncSession = Depends(get_session)):
    employees = await EmployeeService(session).get_employees()
    return employees


@router.get("/{id}")
async def get_employee(id: str, session: AsyncSession = Depends(get_session)):
    employee = await EmployeeService(session).get_employee_by_id(id)
    return employee
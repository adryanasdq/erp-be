from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.schemas.hr.department import Department
from src.core.settings.database import get_session

from .dependency import validate_department
from .service import DepartmentService


router = APIRouter(prefix="/departments", tags=["Departments"])


@router.get("/")
async def get_all_departments(session: AsyncSession = Depends(get_session)):
    departments = await DepartmentService(session).get_all_departments()
    return departments


@router.get("/{id}")
async def get_department(id: str, session: AsyncSession = Depends(get_session)):
    department = await DepartmentService(session).get_department_by_id(id)
    return department


@router.post("/")
async def create_department(
    data: Department, session: AsyncSession = Depends(get_session)
):
    validated_department = await validate_department(data, session)
    return await DepartmentService(session).create_department(validated_department)


@router.put("/{id}")
async def update_department(
    id: str, data: Department, session: AsyncSession = Depends(get_session)
):
    validated_department = await validate_department(data, session, id)
    return await DepartmentService(session).create_department(validated_department)

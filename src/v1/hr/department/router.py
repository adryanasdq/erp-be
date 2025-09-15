from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.schemas.hr.department import Department
from src.core.settings.database import get_session

from .dependency import get_department_by_id, validate_department
from .service import get_all, get_by_id, create, update, delete


router = APIRouter(prefix="/departments", tags=["Departments"])


@router.get("/")
async def get_all_departments(session: AsyncSession = Depends(get_session)):
    departments = await get_all(session)
    return departments


@router.get("/{id}")
async def get_department(id: str, session: AsyncSession = Depends(get_session)):
    department = await get_by_id(id, session)
    return department


@router.post("/")
async def create_department(
    data: Department, session: AsyncSession = Depends(get_session)
):
    validated_department = await validate_department(data, session)
    return await create(validated_department, session)


@router.put("/{id}")
async def update_department(
    id: str, data: Department, session: AsyncSession = Depends(get_session)
):
    validated_department = await validate_department(data, session, id)
    return await update(validated_department, session)


@router.delete("/{id}")
async def delete_department(
    data: Department = Depends(get_department_by_id),
    session: AsyncSession = Depends(get_session),
):
    return await delete(data, session)

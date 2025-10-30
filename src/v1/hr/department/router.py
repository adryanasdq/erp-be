from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as SessionType

from src.core.schemas.hr.department import Department
from src.core.settings.database import get_session

from .dependency import get_department_by_id, validate_department
from .service import get_all, get_by_id, create, update, delete


router = APIRouter(prefix="/departments", tags=["Departments"])


@router.get("/")
def get_all_departments(session = Depends(get_session)):
    departments = get_all(session)
    return departments


@router.get("/{id}")
def get_department(id: str, session = Depends(get_session)):
    department = get_by_id(id, session)
    return department


@router.post("/")
def create_department(
    data: Department, session: SessionType = Depends(get_session)
):
    validated_department = validate_department(data, session)
    return create(validated_department, session)


@router.put("/{id}")
def update_department(
    id: str, data: Department, session: SessionType = Depends(get_session)
):
    validated_department = validate_department(data, session, id)
    return update(validated_department, session)


@router.delete("/{id}")
def delete_department(
    data: Department = Depends(get_department_by_id),
    session: SessionType = Depends(get_session),
):
    return delete(data, session)

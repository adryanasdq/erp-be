from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as SessionType

from src.core.schemas.hr.employee import Employee
from src.core.settings.database import get_session

from .dependency import get_employee_by_id, validate_employee
from .service import get_all, get_by_id, create, update, delete


router = APIRouter(prefix="/employees", tags=["Employees"])


@router.get("/")
def get_all_employees(session = Depends(get_session)):
    employees = get_all(session)
    return employees


@router.get("/{id}")
def get_employee(id: str, session = Depends(get_session)):
    employee = get_by_id(id, session)
    return employee


@router.post("/")
def create_employee(data: Employee, session: SessionType = Depends(get_session)):
    validated_employee = validate_employee(data, session)
    return create(validated_employee, session)


@router.put("/{id}")
def update_employee(
    id: str, data: Employee, session: SessionType = Depends(get_session)
):
    validated_employee = validate_employee(data, session, id)
    return update(validated_employee, session)


@router.delete("/{id}")
def delete_employee(
    data: Employee = Depends(get_employee_by_id),
    session: SessionType = Depends(get_session),
):
    return delete(data, session)
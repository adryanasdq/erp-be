from datetime import datetime
from fastapi import Depends
from sqlmodel import Session as SessionType

from src.core.settings.database import get_session
from src.core.models.hr.department import Department as DbDepartment
from src.core.schemas.hr.department import Department
from src.utils import generate_custom_id

from .exception import DepartmentIdExists, DepartmentNotFound


def check_if_department_exists(dept_id: str, session: SessionType):
    db_dept = session.get(DbDepartment, dept_id)
    if db_dept:
        raise DepartmentIdExists()
    return


def get_department_by_id(
    id: str, session: SessionType = Depends(get_session)
):
    db_dept = session.get(DbDepartment, id)
    if not db_dept:
        raise DepartmentNotFound()
    return db_dept


def validate_department(dept: Department, session: SessionType, id: str = None):
    if id is None:
        dept.id = generate_custom_id("dept", session)
        check_if_department_exists(dept.id, session)
        db_dept = DbDepartment(
            id=dept.id, **dept.model_dump(exclude_unset=True, exclude={"id"})
        )
    else:
        db_dept = get_department_by_id(id, session)
        for key, attr in dept.model_dump(exclude_unset=True).items():
            setattr(db_dept, key, attr)

    db_dept.modified_date = datetime.now()
    return db_dept

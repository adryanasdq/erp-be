from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from src.utils import generate_cuid
from src.core.models.hr.department import Department as DbDepartment
from src.core.schemas.hr.department import Department
from .exception import DepartmentIdExists, DepartmentNotFound

async def check_if_department_exists(dept_id: str, session: AsyncSession):
    db_dept = await session.get(DbDepartment, dept_id)
    if db_dept:
        raise DepartmentIdExists()
    return

async def get_department_by_id(dept_id: str, session: AsyncSession):
    db_dept = await session.get(DbDepartment, dept_id)
    if not db_dept:
        raise DepartmentNotFound()
    return db_dept

async def validate_department(dept: Department, session: AsyncSession, id: str = None):
    if id is None:
        dept.id = generate_cuid()
        await check_if_department_exists(dept.id, session)
        db_dept = DbDepartment(
            id=dept.id, **dept.model_dump(exclude_unset=True, exclude={"id"})
        )
    else:
        db_dept = await get_department_by_id(id, session)
        for key, attr in dept.model_dump(exclude_unset=True).items():
            setattr(db_dept, key, attr)

    db_dept.modified_date = datetime.now()
    return db_dept

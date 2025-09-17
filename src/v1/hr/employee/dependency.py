from datetime import datetime
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.settings.database import get_session
from src.core.models.hr.employee import Employee as DbEmployee
from src.core.schemas.hr.employee import Employee
from src.utils import generate_custom_id
from src.v1.hr.position.dependency import get_position_by_id

from .exception import EmployeeIdExists, EmployeeNotFound


async def check_if_employee_exists(emp_id: str, session: AsyncSession):
    db_emp = await session.get(DbEmployee, emp_id)
    if db_emp:
        raise EmployeeIdExists()
    return


async def get_employee_by_id(
    emp_id: str, session: AsyncSession = Depends(get_session)
):
    db_emp = await session.get(DbEmployee, emp_id)
    if not db_emp:
        raise EmployeeNotFound()
    return db_emp


async def validate_employee(employee: Employee, session: AsyncSession, id: str = None):
    await get_position_by_id(employee.position_id, session)

    if id is None:
        employee.id = await generate_custom_id("emp", session)
        await check_if_employee_exists(employee.id, session)
        db_emp = DbEmployee(
            id=employee.id, **employee.model_dump(exclude_unset=True, exclude={"id"})
        )
    else:
        db_emp = await get_employee_by_id(id, session)
        for key, attr in employee.model_dump(exclude_unset=True).items():
            setattr(db_emp, key, attr)

    db_emp.modified_date = datetime.now()
    return db_emp
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.schemas.hr.employee import Employee


def validate_employee(employee: Employee, session: AsyncSession, id: str = None):
    # validate pos_id
    # validate dept_id

    return
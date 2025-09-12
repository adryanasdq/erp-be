from sqlalchemy.ext.asyncio import AsyncSession

from src.core.schemas.hr.employee import CreateEmployee


def validate_employee(employee: CreateEmployee, session: AsyncSession, id: str = None):
    # validate pos_id
    # validate dept_id

    return
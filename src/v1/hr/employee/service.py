from fastapi import HTTPException
from sqlmodel import select
from sqlalchemy.orm import Session as SessionType

from src.core.models.hr.employee import Employee as DbEmployee
from src.core.schemas.hr.employee import Employee


def get_all(session):
    stmnt = select(DbEmployee)

    result = session.execute(stmnt)
    return result.scalars().all()


def get_by_id(employee_id: str, session):
    stmnt = select(DbEmployee).where(DbEmployee.id == employee_id)

    result = session.execute(stmnt)
    return result.scalar_one_or_none()


def create(employee: DbEmployee, session: SessionType):
    try:
        session.add(employee)
        session.commit()
        session.refresh(employee)
        return Employee.model_validate(employee)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    

def update(employee: DbEmployee, session: SessionType):
    try:
        session.commit()
        session.refresh(employee)
        return Employee.model_validate(employee)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    

def delete(employee: DbEmployee, session: SessionType):
    try:
        session.delete(employee)
        session.commit()
        return {"message": f"Employee with id {employee.id} deleted successfully"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
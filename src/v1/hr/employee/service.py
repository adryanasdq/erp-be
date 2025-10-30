from fastapi import HTTPException
from sqlmodel import select, Session as SessionType

from src.core.models.hr.employee import Employee as DbEmployee
from src.core.schemas.hr.employee import Employee


def get_all(session: SessionType):
    stmnt = select(DbEmployee)

    result = session.exec(stmnt)
    return result.all()


def get_by_id(employee_id: str, session: SessionType):
    stmnt = select(DbEmployee).where(DbEmployee.id == employee_id)

    result = session.exec(stmnt)
    return result.first()


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
from fastapi import HTTPException
from sqlmodel import select
from sqlalchemy.orm import Session as SessionType

from src.core.models.hr.department import Department as DbDepartment
from src.core.schemas.hr.department import Department


def get_all(session):
    stmnt = select(DbDepartment)

    result = session.execute(stmnt)
    return result.scalars().all()


def get_by_id(department_id: str, session):
    stmnt = select(DbDepartment).where(DbDepartment.id == department_id)

    result = session.execute(stmnt)
    return result.scalar_one_or_none()


def create(department: DbDepartment, session: SessionType):
    try:
        session.add(department)
        session.commit()
        session.refresh(department)
        return Department.model_validate(department)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def update(department: DbDepartment, session: SessionType):
    try:
        session.commit()
        session.refresh(department)
        return Department.model_validate(department)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    

def delete(department: DbDepartment, session: SessionType):
    try:
        session.delete(department)
        session.commit()
        return {"message": f"Department with id {department.id} deleted successfully"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
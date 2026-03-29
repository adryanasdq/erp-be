from fastapi import HTTPException
from sqlmodel import select, Session as SessionType

from src.core.models.sales.customer import Customer as DbCustomer
from src.core.schemas.sales.customer import Customer


def get_all(session: SessionType):
    stmnt = select(DbCustomer)
    result = session.exec(stmnt)
    return result.all()


def get_by_id(customer_id: str, session: SessionType):
    stmnt = select(DbCustomer).where(DbCustomer.id == customer_id)
    result = session.exec(stmnt)
    return result.first()


def create(customer: DbCustomer, session: SessionType):
    try:
        session.add(customer)
        session.commit()
        session.refresh(customer)
        return Customer.model_validate(customer)
    except Exception as e:
        session.rollback()
        # Mirroring your pattern of 400 for DB errors
        raise HTTPException(status_code=400, detail=str(e))


def update(customer: DbCustomer, session: SessionType):
    try:
        session.commit()
        session.refresh(customer)
        return Customer.model_validate(customer)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def delete(customer: DbCustomer, session: SessionType):
    try:
        session.delete(customer)
        session.commit()
        return {"message": f"Customer with id {customer.id} deleted successfully"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
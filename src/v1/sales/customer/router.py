from fastapi import APIRouter, Depends
from sqlmodel import Session as SessionType
from src.core.settings.database import get_session
from src.core.schemas.sales.customer import Customer
from .dependency import (
    get_customer_by_id,
    validate_customer,
    validate_customer_deletion,
)
from .service import get_all, create, delete, update

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.get("/")
def get_customers(session: SessionType = Depends(get_session)):
    return get_all(session)


@router.get("/{id}")
def get_customer(id: str, session: SessionType = Depends(get_session)):
    return get_customer_by_id(id, session)


@router.post("/")
def create_customer(data: Customer, session: SessionType = Depends(get_session)):
    validated = validate_customer(data, session)
    return create(validated, session)


@router.put("/{id}")
def update_customer(
    id: str, data: Customer, session: SessionType = Depends(get_session)
):
    validated_customer = validate_customer(data, session, id)
    return update(validated_customer, session)


@router.delete("/{id}")
def delete_customer(id: str, session: SessionType = Depends(get_session)):
    db_cust = validate_customer_deletion(id, session)
    return delete(db_cust, session)

from fastapi import APIRouter, Depends
from sqlmodel import Session as SessionType
from src.core.settings.database import get_session
from src.core.schemas.sales.customer import Customer
from .dependency import get_customer_by_id, validate_customer
from .service import get_all, create # Assume standard get_all/create in service

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.get("/")
def get_customers(session: SessionType = Depends(get_session)):
    return get_all(session)

@router.post("/")
def create_customer(data: Customer, session: SessionType = Depends(get_session)):
    validated = validate_customer(data, session)
    return create(validated, session)
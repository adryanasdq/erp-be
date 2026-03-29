from datetime import datetime
from fastapi import Depends
from sqlmodel import Session as SessionType, select
from src.core.settings.database import get_session
from src.core.models.sales.customer import Customer as DbCustomer
from src.core.schemas.sales.customer import Customer

from src.core.models.sales.sales_order import SalesOrder as DbSO

from .exception import CustomerNotFound, CustomerCodeExists, CustomerHasTransactions


def get_customer_by_id(id: str, session: SessionType = Depends(get_session)):
    db_customer = session.get(DbCustomer, id)
    if not db_customer:
        raise CustomerNotFound()
    return db_customer


def validate_customer(customer: Customer, session: SessionType, id: str = None):
    if not id:
        stmnt = select(DbCustomer).where(DbCustomer.code == customer.code)
        existing = session.exec(stmnt).first()
        if existing:
            raise CustomerCodeExists()
        db_customer = DbCustomer(**customer.model_dump(exclude={"id"}))
    else:
        db_customer = get_customer_by_id(id, session)
        for key, attr in customer.model_dump(exclude_unset=True).items():
            setattr(db_customer, key, attr)

    db_customer.modified_date = datetime.now()
    return db_customer


def validate_customer_deletion(customer_id: str, session: SessionType):
    db_customer = get_customer_by_id(customer_id, session)

    has_orders = session.exec(select(DbSO).where(DbSO.customer_id == customer_id)).first()
    if has_orders:
        raise CustomerHasTransactions()

    return db_customer

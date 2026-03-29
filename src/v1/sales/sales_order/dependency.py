from datetime import datetime
from fastapi import Depends
from sqlmodel import Session as SessionType, select
from src.core.settings.database import get_session
from src.core.models.sales.sales_order import SalesOrder as DbSO, SalesOrderLine as DbSOLine
from src.core.schemas.sales.sales_order import SalesOrderSchema

from ..customer.dependency import get_customer_by_id
from ...inventory.warehouse.dependency import get_warehouse_by_id
from .exception import SONotFound, SONumberExists

def get_so_by_id(id: str, session: SessionType = Depends(get_session)):
    db_so = session.get(DbSO, id)
    if not db_so:
        raise SONotFound()
    return db_so

def validate_so(data: SalesOrderSchema, session: SessionType, id: str = None):
    get_customer_by_id(data.customer_id, session)
    get_warehouse_by_id(data.warehouse_id, session)

    if not id:
        existing = session.exec(select(DbSO).where(DbSO.so_number == data.so_number)).first()
        if existing:
            raise SONumberExists()

        db_so = DbSO(**data.model_dump(exclude={"id", "lines"}))
        db_so.lines = [DbSOLine(**line.model_dump()) for line in data.lines]
    else:
        db_so = get_so_by_id(id, session)
        # Update logic similar to PO...
    
    db_so.modified_date = datetime.now()
    return db_so
from datetime import datetime
from fastapi import Depends
from sqlmodel import Session as SessionType, select

from src.core.settings.database import get_session
from src.core.models.purchasing.supplier import Supplier as DbSupplier
from src.core.schemas.purchasing.supplier import Supplier

from .exception import SupplierNotFound, SupplierCodeExists 


def get_supplier_by_id(
    id: str, session: SessionType = Depends(get_session)
):
    db_supplier = session.get(DbSupplier, id)
    if not db_supplier:
        raise SupplierNotFound()
    return db_supplier


def validate_supplier(supplier: Supplier, session: SessionType, id: str = None):
    if not id:
        existing = session.exec(
            select(DbSupplier).where(DbSupplier.code == supplier.code)
        ).first()
        if existing:
            raise SupplierCodeExists()
            
        db_supplier = DbSupplier(
            **supplier.model_dump(exclude_unset=True, exclude={"id"})
        )
    else:
        db_supplier = get_supplier_by_id(id, session)
        for key, attr in supplier.model_dump(exclude_unset=True).items():
            setattr(db_supplier, key, attr)

    db_supplier.modified_date = datetime.now()
    return db_supplier
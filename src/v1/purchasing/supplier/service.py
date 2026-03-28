from fastapi import HTTPException
from sqlmodel import select, Session as SessionType

from src.core.models.purchasing.supplier import Supplier as DbSupplier
from src.core.schemas.purchasing.supplier import Supplier


def get_all(session: SessionType):
    stmnt = select(DbSupplier)
    result = session.exec(stmnt)
    return result.all()


def get_by_id(supplier_id: str, session: SessionType):
    stmnt = select(DbSupplier).where(DbSupplier.id == supplier_id)
    result = session.exec(stmnt)
    return result.first()


def create(supplier: DbSupplier, session: SessionType):
    try:
        session.add(supplier)
        session.commit()
        session.refresh(supplier)
        return Supplier.model_validate(supplier)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def update(supplier: DbSupplier, session: SessionType):
    try:
        session.commit()
        session.refresh(supplier)
        return Supplier.model_validate(supplier)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def delete(supplier: DbSupplier, session: SessionType):
    try:
        session.delete(supplier)
        session.commit()
        return {"message": f"Supplier with id {supplier.id} deleted successfully"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
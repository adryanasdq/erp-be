from fastapi import HTTPException
from sqlmodel import select, Session as SessionType
from src.core.models.purchasing.purchase_order import PurchaseOrder as DbPO
from src.core.schemas.purchasing.purchase_order import PurchaseOrderSchema


def get_all(session: SessionType):
    # Using select(DbPO) will include lines if the Relationship is lazy='joined' 
    # or accessed later in the same session.
    stmnt = select(DbPO)
    result = session.exec(stmnt)
    return result.all()


def get_by_id(po_id: str, session: SessionType):
    stmnt = select(DbPO).where(DbPO.id == po_id)
    result = session.exec(stmnt)
    return result.first()


def create(po: DbPO, session: SessionType):
    try:
        session.add(po)
        # SQLAlchemy/SQLModel handles the child lines automatically 
        # because of the Relationship(back_populates="purchase_order")
        session.commit()
        session.refresh(po)
        return po
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def update(po: DbPO, session: SessionType):
    try:
        session.commit()
        session.refresh(po)
        return po
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def delete(po: DbPO, session: SessionType):
    try:
        session.delete(po)
        session.commit()
        return {"message": f"PO {po.po_number} deleted successfully"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
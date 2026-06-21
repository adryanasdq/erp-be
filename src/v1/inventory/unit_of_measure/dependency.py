from datetime import datetime
from fastapi import Depends
from sqlmodel import Session as SessionType, select, or_

from src.core.settings.database import get_session
from src.core.models.inventory.uom import UnitOfMeasure as DbUnitOfMeasure
from src.core.schemas.inventory.uom import UnitOfMeasure

from .exception import UnitOfMeasureExists, UnitOfMeasureNotFound


def check_if_uom_exists(uom: UnitOfMeasure, session: SessionType):
    statement = select(DbUnitOfMeasure).where(
        or_(
            DbUnitOfMeasure.name == uom.name,
            DbUnitOfMeasure.symbol == uom.symbol
        )
    )
    db_uom = session.exec(statement).first()
    if db_uom:
        raise UnitOfMeasureExists(uom)
    return


def get_uom_by_id(
    id: str, session: SessionType = Depends(get_session)
):
    db_uom = session.get(DbUnitOfMeasure, id)
    if not db_uom:
        raise UnitOfMeasureNotFound()
    return db_uom


def validate_uom(uom: UnitOfMeasure, session: SessionType, id: str = None):
    if not id:
        check_if_uom_exists(uom, session)

        db_uom = DbUnitOfMeasure(
            **uom.model_dump(exclude_unset=True, exclude={"id"})
        )
    else:
        db_uom = get_uom_by_id(id, session)
        for key, attr in uom.model_dump(exclude_unset=True).items():
            setattr(db_uom, key, attr)

    db_uom.modified_date = datetime.now()
    return db_uom
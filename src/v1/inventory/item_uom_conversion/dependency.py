from fastapi import Depends
from sqlmodel import select, Session as SessionType

from src.core.settings.database import get_session
from src.core.models.inventory.item_uom_conversion import (
    ItemUOMConversion as DbItemUOMConversion,
)
from src.core.schemas.inventory.item_uom_conversion import ItemUOMConversion

from src.v1.inventory.item.dependency import get_item_by_id
from src.v1.inventory.unit_of_measure.dependency import get_uom_by_id

from .exception import (
    ItemUOMConversionIdExists,
    ItemUOMConversionNotFound,
    ItemUOMConversionIncompatible,
)


def check_if_uom_exists(conv_id: str, session: SessionType):
    db_item_uom_conv = session.get(DbItemUOMConversion, conv_id)
    if db_item_uom_conv:
        raise ItemUOMConversionIdExists()
    return


def get_item_uom_conv_by_id(id: str, session: SessionType = Depends(get_session)):
    db_item_uom_conv = session.get(DbItemUOMConversion, id)
    if not db_item_uom_conv:
        raise ItemUOMConversionNotFound()
    return db_item_uom_conv


def get_conv_factor_to_base(item_id: str, from_uom_id: str, session: SessionType):
    db_item = get_item_by_id(item_id, session)
    if db_item.uom_id == from_uom_id:
        return 1

    conversion = get_item_uom_conv_by_uom_id(from_uom_id, db_item.uom_id, session)
    return conversion.factor


def get_item_uom_conv_by_uom_id(from_uom_id: str, to_uom_id: str, session: SessionType):
    stmnt = select(DbItemUOMConversion).where(
        DbItemUOMConversion.from_uom_id == from_uom_id,
        DbItemUOMConversion.to_uom_id == to_uom_id,
        DbItemUOMConversion.is_active,
    )
    query = session.exec(stmnt)
    db_item_uom_conv = query.first()

    if not db_item_uom_conv:
        raise ItemUOMConversionNotFound()
    return db_item_uom_conv


def validate_item_uom_conv(
    conv: ItemUOMConversion, session: SessionType, id: str = None
):
    from_uom = get_uom_by_id(conv.from_uom_id, session)
    to_uom = get_uom_by_id(conv.to_uom_id, session)

    if from_uom.type != to_uom.type:
        raise ItemUOMConversionIncompatible()

    if not id:
        db_item_uom_conv = DbItemUOMConversion(
            **conv.model_dump(exclude_unset=True, exclude={"id"})
        )
    else:
        db_item_uom_conv = get_item_uom_conv_by_id(id, session)
        for key, attr in conv.model_dump(exclude_unset=True).items():
            setattr(db_item_uom_conv, key, attr)

    return db_item_uom_conv

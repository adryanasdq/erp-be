from fastapi import APIRouter, Depends
from sqlmodel import Session as SessionType

from src.core.schemas.inventory.item_uom_conversion import ItemUOMConversion
from src.core.settings.database import get_session

from .dependency import get_item_uom_conv_by_id, validate_item_uom_conv
from .service import get_all, get_by_id, create, unactive


router = APIRouter(prefix="/item_uom_conversion", tags=["Item UOM Conversion"])


@router.get("/")
def get_all_conversions(session=Depends(get_session)):
    conversions = get_all(session)
    return conversions


@router.get("/{id}")
def get_conversion_by_id(id: str, session=Depends(get_session)):
    conversion = get_by_id(id, session)
    return conversion


@router.post("/")
def create_conversion(data: ItemUOMConversion, session: SessionType = Depends(get_session)):
    validated_item_uom_conv = validate_item_uom_conv(data, session)
    return create(validated_item_uom_conv, session)


@router.patch("/")
def unactive_conversion(
    data: ItemUOMConversion = Depends(get_item_uom_conv_by_id),
    session: SessionType = Depends(get_session),
):
    return unactive(data, session)

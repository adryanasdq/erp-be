from fastapi import APIRouter, Depends
from sqlmodel import Session as SessionType

from src.core.schemas.inventory.stock_movement import StockMovement, StockTransfer
from src.core.settings.database import get_session

from src.v1.inventory.stock_balance.dependency import validate_stock_balance

from .dependency import validate_stock_movement, validate_stock_transfer
from .service import get_all, get_by_id, create, transfer


router = APIRouter(prefix="/stock_movement", tags=["Stock Movements"])


@router.get("/")
def get_all_stock_movements(session=Depends(get_session)):
    stock_movements = get_all(session)
    return stock_movements


@router.get("/{id}")
def get_stock_movement(id: str, session=Depends(get_session)):
    stock_movement = get_by_id(id, session)
    return stock_movement


@router.post("/")
def create_stock_movement(
    data: StockMovement, session: SessionType = Depends(get_session)
):
    validated_stock_movement = validate_stock_movement(data, session)
    validated_stock_balance = validate_stock_balance(data, session)
    return create(validated_stock_movement, validated_stock_balance, session)


# @router.post("/transfer")
# def create_transfer_movement(
#     data: StockTransfer, session: SessionType = Depends(get_session)
# ):
#     validated_stock_transfer = validate_stock_transfer(data, session)
#     return transfer(validated_stock_transfer, session)

from fastapi import APIRouter, Depends

from src.core.schemas.inventory.item import Item
from src.core.settings.database import get_session

from .service import get_all, get_by_id


router = APIRouter(prefix="/stock_balances", tags=["Stock Balances"])


@router.get("/")
def get_all_stock_balances(session=Depends(get_session)):
    stock_balances = get_all(session)
    return stock_balances


@router.get("/{id}")
def get_stock_balance(id: str, session=Depends(get_session)):
    stock_balance = get_by_id(id, session)
    return stock_balance
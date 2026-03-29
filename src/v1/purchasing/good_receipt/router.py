from fastapi import APIRouter, Depends
from sqlmodel import Session as SessionType
from src.core.settings.database import get_session
from src.core.schemas.purchasing.goods_receipt import GoodsReceiptSchema
from .dependency import validate_grn_processing
from .service import commit_grn_transaction

router = APIRouter(prefix="/goods-receipts", tags=["Goods Receipt (GRN)"])

@router.post("/")
def create_grn(data: GoodsReceiptSchema, session: SessionType = Depends(get_session)):
    processed_data = validate_grn_processing(data, session)
    
    return commit_grn_transaction(processed_data, session)
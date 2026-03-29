from fastapi import APIRouter, Depends
from sqlmodel import Session as SessionType
from src.core.settings.database import get_session
from src.core.schemas.sales.delivery import DeliverySchema
from .dependency import validate_delivery_processing
from .service import commit_delivery_transaction


router = APIRouter(prefix="/deliveries", tags=["Deliveries"])

@router.post("/")
def create_delivery(data: DeliverySchema, session: SessionType = Depends(get_session)):
    processed_data = validate_delivery_processing(data, session)
    
    return commit_delivery_transaction(processed_data, session)

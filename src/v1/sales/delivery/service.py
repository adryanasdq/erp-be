from fastapi import HTTPException
from sqlmodel import Session as SessionType

def commit_delivery_transaction(processed_data: dict, session: SessionType):
    try:
        # Add the Delivery Header & Lines
        session.add(processed_data["delivery"])
        
        # Add all pre-calculated Inventory movements/balances
        for mov, bal in processed_data["inventory_updates"]:
            session.add(mov)
            session.add(bal)
            
        session.commit()
        session.refresh(processed_data["delivery"])
        return processed_data["delivery"]
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
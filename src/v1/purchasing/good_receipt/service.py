from fastapi import HTTPException
from sqlmodel import Session as SessionType

def commit_grn_transaction(processed_data: dict, session: SessionType):
    try:
        # 1. Add GRN Header & Lines
        session.add(processed_data["grn"])
        
        # 2. Add all pre-calculated Inventory movements/balances
        for mov, bal in processed_data["inventory_updates"]:
            session.add(mov)
            session.add(bal)
            
        session.commit()
        session.refresh(processed_data["grn"])
        return processed_data["grn"]
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
from fastapi import HTTPException

class DeliveryNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Delivery record not found.")

class SODeliveryNotConfirmed(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Sales Order must be CONFIRMED to create a Delivery.")

class DeliveryQtyExceedsOrder(HTTPException):
    def __init__(self, item_id: str):
        super().__init__(status_code=400, detail=f"Delivery quantity for {item_id} exceeds remaining ordered quantity.")

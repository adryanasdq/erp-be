from fastapi import HTTPException

class SODeliveryNotConfirmed(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Sales Order must be Confirmed or Partially Delivered to create a Delivery.")

class DeliveryQtyExceedsReserved(HTTPException):
    def __init__(self, item_code: str):
        super().__init__(status_code=400, detail=f"Delivery quantity for {item_code} exceeds the reserved amount.")
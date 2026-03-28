from fastapi import HTTPException


class PONumberExists(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="PO Number already exists. Try again.")


class PONotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Purchase Order is not found.")
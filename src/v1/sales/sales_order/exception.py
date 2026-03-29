from fastapi import HTTPException


class SONotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Sales Order is not found.")


class SONumberExists(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Sales Order Number already exists. Try again.")
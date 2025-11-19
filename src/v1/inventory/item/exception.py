from fastapi import HTTPException


class ItemIdExists(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Item ID already exists. Try again.")


class ItemNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Item is not found.")
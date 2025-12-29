from fastapi import HTTPException


class StockMovementIdExists(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400, detail="Stock Movement ID already exists. Try again."
        )

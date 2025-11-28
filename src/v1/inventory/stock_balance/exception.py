from fastapi import HTTPException


class StockBalanceIdExists(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Stock Balance ID already exists. Try again.")


class StockBalanceNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Stock Balance is not found.")
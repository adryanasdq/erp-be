from fastapi import HTTPException


class StockBalanceInsufficent(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Stock Balance for this item is not sufficent to OUT/TRANSFER")

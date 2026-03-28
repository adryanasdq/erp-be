from fastapi import HTTPException


class GRNNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Goods Receipt is not found.")
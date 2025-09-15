from fastapi import HTTPException


class PositionIdExists(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Position ID already exists. Try again.")


class PositionNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Position is not found.")
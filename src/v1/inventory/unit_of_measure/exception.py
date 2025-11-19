from fastapi import HTTPException


class UnitOfMeasureIdExists(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Unit Of Measure ID already exists. Try again.")


class UnitOfMeasureNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Unit Of Measure is not found.")
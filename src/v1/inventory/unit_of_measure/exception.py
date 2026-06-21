from fastapi import HTTPException

from src.core.schemas.inventory.uom import UnitOfMeasure


class UnitOfMeasureExists(HTTPException):
    def __init__(self, uom: UnitOfMeasure):
        super().__init__(status_code=400, detail=f"Unit Of Measure {uom.name}({uom.symbol}) is already exists.")


class UnitOfMeasureNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Unit Of Measure is not found.")

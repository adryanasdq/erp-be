from fastapi import HTTPException


class WarehouseExists(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Warehouse is already exists.")


class WarehouseNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Warehouse is not found.")
from fastapi import HTTPException


class WarehouseIdExists(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Warehouse ID already exists. Try again.")


class WarehouseNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Warehouse is not found.")
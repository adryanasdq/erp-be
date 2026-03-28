from fastapi import HTTPException


class SupplierCodeExists(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Supplier Code already exists. Try again.")


class SupplierNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Supplier is not found.")
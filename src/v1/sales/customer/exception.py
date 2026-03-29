from fastapi import HTTPException


class CustomerCodeExists(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Customer Code already exists. Try again.")


class CustomerNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Customer is not found.")
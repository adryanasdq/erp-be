from fastapi import HTTPException


class AccountNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Chart of Account not found.")


class AccountCodeExists(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Account code already exists.")

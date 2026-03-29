from fastapi import HTTPException


class CustomerNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Customer not found.")


class CustomerCodeExists(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Customer code already exists.")


class CustomerHasTransactions(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Cannot delete customer with existing sales history.",
        )

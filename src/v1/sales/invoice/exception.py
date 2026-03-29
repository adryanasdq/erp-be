from fastapi import HTTPException


class InvoiceNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Invoice not found.")


class DuplicateInvoiceNumber(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Invoice number already exists.")

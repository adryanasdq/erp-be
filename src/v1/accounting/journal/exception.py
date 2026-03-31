from fastapi import HTTPException


class JournalUnbalanced(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400, detail="Total Debits must equal Total Credits."
        )


class JournalEntryNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Journal Entry not found.")


class AccountNotFound(HTTPException):
    def __init__(self, code: str):
        super().__init__(status_code=404, detail=f"Account with code {code} not found.")

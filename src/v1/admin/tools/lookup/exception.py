from fastapi import HTTPException


class GroupCodeNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Group code is not found.")


class OptionAlreadyExists(HTTPException):
    def __init__(self, value: str):
        super().__init__(status_code=400, detail=f"Option {value} is already exists in this group code")


class OptionNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Option is not found")
from fastapi import HTTPException


class DepartmentIdExists(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Department ID already exists. Try again.")


class DepartmentNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Department is not found.")
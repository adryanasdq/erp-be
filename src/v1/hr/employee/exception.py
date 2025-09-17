from fastapi import HTTPException


class EmployeeIdExists(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Employee ID already exists. Try again.")


class EmployeeNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Employee is not found.")
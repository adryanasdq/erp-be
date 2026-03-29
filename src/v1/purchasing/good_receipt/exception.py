from fastapi import HTTPException


class GRNNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Goods Receipt Note not found.")

class PONotApproved(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Purchase Order must be APPROVED to receive goods.")
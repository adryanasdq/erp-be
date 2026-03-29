from fastapi import HTTPException


class GRNNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Goods Receipt Note not found.")


class GRNCancelForbidden(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Cannot cancel a GRN that has already been invoiced.",
        )


class PONotApproved(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400, detail="Purchase Order must be APPROVED to receive goods."
        )

class GRNAlreadyCanceled(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Cannot cancel a GRN that has already been canceled.",
        )

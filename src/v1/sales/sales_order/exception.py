from fastapi import HTTPException


class SONotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Sales Order not found.")


class SONumberExists(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Sales Order number already exists.")


class SOInsufficientStock(HTTPException):
    def __init__(self, item_id: str, available: float):
        super().__init__(
            status_code=400,
            detail=f"Insufficient stock for item {item_id}. Available: {available}",
        )


class SOInvalidStatus(HTTPException):
    def __init__(self, current_status: str):
        super().__init__(
            status_code=400, detail=f"Action not allowed for status: {current_status}"
        )


class SOCancelForbidden(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Cannot cancel a Sales Order that has already been delivered.",
        )

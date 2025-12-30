from fastapi import HTTPException


class ItemUOMConversionIdExists(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400, detail="Item UOM Conversion ID already exists. Try again."
        )


class ItemUOMConversionAlreadyExists(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="This conversion already exists.")


class ItemUOMConversionNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Item UOM Conversion is not found.")


class ItemUOMConversionIncompatible(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Cannot create conversion with different types of UOMs.",
        )

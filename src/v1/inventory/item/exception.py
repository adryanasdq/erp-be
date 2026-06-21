from fastapi import HTTPException


class ItemSKUExists(HTTPException):
    def __init__(self, sku:str):
        super().__init__(status_code=400, detail=f"Item with SKU {sku} already exists.")


class ItemNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Item is not found.")
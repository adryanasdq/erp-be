from pydantic import BaseModel

class AccountSchema(BaseModel):
    code: str
    name: str
    type: str
    active: bool = True

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "code": "1010",
                "name": "Inventory - Raw Materials",
                "type": "ASSET",
                "active": True
            }
        }
    }
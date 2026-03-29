from pydantic import BaseModel


class InvoiceSchema(BaseModel):
    invoice_number: str
    delivery_id: str
    customer_id: str
    total_amount: float

    model_config = {
        "from_attributes": True,
        "example": {
            "invoice_number": "INV-2026-001",
            "delivery_id": "89c74b9e-...",
            "customer_id": "a1b2c3d4-...",
            "total_amount": 1250.50,
            "date": "2026-03-29T10:00:00",
        },
    }

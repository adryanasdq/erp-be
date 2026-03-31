from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime


class JournalLineSchema(BaseModel):
    account_id: str
    debit: float = 0.0
    credit: float = 0.0


class JournalEntrySchema(BaseModel):
    date: Optional[datetime] = None
    reference_type: str
    reference_id: Optional[str] = None
    description: Optional[str] = None
    lines: List[JournalLineSchema]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "date": "2026-03-31T15:00:00",
                "reference_type": "MANUAL",
                "reference_id": "REF-001",
                "description": "Initial Capital Investment",
                "lines": [
                    {"account_id": "cl_cash_cuid_123", "debit": 5000.0, "credit": 0.0},
                    {
                        "account_id": "cl_equity_cuid_456",
                        "debit": 0.0,
                        "credit": 5000.0,
                    },
                ],
            }
        }
    )

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class JournalLineSchema(BaseModel):
    account_id: str
    debit: float = 0.0
    credit: float = 0.0


class JournalEntrySchema(BaseModel):
    date: Optional[datetime] = None
    reference_type: str
    reference_id: str
    description: Optional[str] = None
    lines: List[JournalLineSchema]

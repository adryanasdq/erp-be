from fastapi import APIRouter

from src.v1.accounting.journal.router import router as journal_router


accounting_router = APIRouter(prefix="/accounting")

accounting_router.include_router(journal_router)

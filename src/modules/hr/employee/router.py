from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_session


router = APIRouter(prefix="/employees", tags=["Employees"])

@router.get("/")
async def get_employees():
    return {"message": "List of employees"}
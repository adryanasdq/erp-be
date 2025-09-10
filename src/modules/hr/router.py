from fastapi import APIRouter

from src.modules.hr.employee.router import router as employee_router

hr_router = APIRouter(prefix="/hr")

hr_router.include_router(employee_router)
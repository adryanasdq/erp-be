from fastapi import APIRouter

from src.v1.hr.employee.router import router as employee_router
from src.v1.hr.department.router import router as department_router

hr_router = APIRouter(prefix="/hr")

hr_router.include_router(department_router)
hr_router.include_router(employee_router)
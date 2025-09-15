from fastapi import APIRouter

from src.v1.hr.employee.router import router as employee_router
from src.v1.hr.department.router import router as department_router
from src.v1.hr.position.router import router as position_router

hr_router = APIRouter(prefix="/hr")

hr_router.include_router(department_router)
hr_router.include_router(employee_router)
hr_router.include_router(position_router)
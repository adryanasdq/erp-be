from fastapi import APIRouter

from src.v1.admin.tools.router import admin_tools_router

admin_router = APIRouter(prefix="/admin")

admin_router.include_router(admin_tools_router)
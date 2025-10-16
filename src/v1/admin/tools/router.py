from fastapi import APIRouter

from src.v1.admin.tools.menu.router import router as menu_router

admin_tools_router = APIRouter(prefix="/tools")

admin_tools_router.include_router(menu_router)
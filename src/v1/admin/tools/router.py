from fastapi import APIRouter

from src.v1.admin.tools.menu.router import router as menu_router
from src.v1.admin.tools.lookup.router import router as lookup_router

admin_tools_router = APIRouter(prefix="/tools")

admin_tools_router.include_router(menu_router)
admin_tools_router.include_router(lookup_router)
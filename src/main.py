from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from src.core.settings.database import init_db
from src.v1.admin.router import admin_router
from src.v1.hr.router import hr_router


def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="ERP",
    description="Enterprise Resource Planning System",
    version="1.0.0",
    lifespan=lifespan
)

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(admin_router)
api_router.include_router(hr_router)

app.include_router(api_router)

def main():
    import uvicorn
    uvicorn.run("src.main:app", port=5000, reload=True, log_level="info")

if __name__ == "__main__":
    main()

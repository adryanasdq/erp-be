from fastapi import FastAPI, APIRouter
# from fastapi.exceptions import HTTPException
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from src.core.db import init_db
from src.modules.hr.router import hr_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(
    title="ERP",
    description="Enterprise Resource Planning System",
    version="1.0.0",
    lifespan=lifespan
)

origins = [
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(hr_router)

app.include_router(api_router)

def main():
    import uvicorn
    uvicorn.run("main:app", port=5000, reload=True, log_level="info")

if __name__ == "__main__":
    main()

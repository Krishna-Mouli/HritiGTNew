from fastapi import APIRouter
from .searchapis import router as search_router
from .filesapis import router as ingestion_router

api_router = APIRouter()

api_router.include_router(search_router, prefix="/api/v1/search", tags = ["search"])
api_router.include_router(ingestion_router, prefix="/api/v1/ingestion", tags = ["ingestion"])
from fastapi import APIRouter
from .searchapis import router as search_router
from .conversationapis import router as conversation_router
from .conferencerooms import router as conference_room_router

api_router = APIRouter()

api_router.include_router(search_router, prefix="/api/search", tags = ["search"])
api_router.include_router(conversation_router, prefix = "/api/conversation", tags = ["conversation"])
api_router.include_router(conference_room_router, prefix = "/api/conferencerooms", tags = ["conferencerooms"])

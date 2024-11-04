import logging
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from Data.Models import SearchRequest
from Services import RAG

router = APIRouter()

@router.post("/apps/{appid}/conversations/{conversationid}")
async def Search(appid: str, conversationid: str, req: SearchRequest):
    try:
        resp = await RAG().search(convo_id = conversationid, app_id = appid, question = req.searchrequest)
        return JSONResponse(
            content = resp,
            status_code = 200
        )
    except Exception as e:
        return JSONResponse(
            content = f"Error {e}",
            status_code = 500
        )
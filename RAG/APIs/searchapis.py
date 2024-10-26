import logging
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from Data.Models import SearchRequest

router = APIRouter()

@router.post("/apps/{appid}/conversations/{conversationid}")
async def Search(req: SearchRequest):
    try:
        #search logic
        print('Searching')
    except Exception as e:
        print('Error')
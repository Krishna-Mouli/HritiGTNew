from fastapi import APIRouter
from Data.Models.conversereq import ConverseRequest 
from Services import SearchService, GCPStorageServiceClient
from fastapi.responses import JSONResponse
from openai.types.chat import ChatCompletionMessage

router = APIRouter()

@router.post("/chat")
async def converse(req: ConverseRequest):
    try:
        _searchservice = SearchService()
        _googlecloudstorageservice = GCPStorageServiceClient()
        conve_id = '891adase13e2-12128duqwd1-12'
        if req is None:
            return JSONResponse(
                status_code=400,    
                content = {"error": "Non data provided in the payload"}
            )
        message_history = _googlecloudstorageservice.get_conversations(conversation_id = conve_id)
        if message_history is None:
            message_history = []
        question = req.message
        if question is None:    
            return JSONResponse(
                status_code=400,
                content = {"error": "No question provided"}
            )
        response = _searchservice.search( question, message_history)
        final_answer = []
        for item in response:
            if isinstance(item, ChatCompletionMessage):
                ans = item.content
                role = item.role
            else:
                ans = item.get('content')
                role = item.get('role')
            if ans is not None and role is not None and role.lower() != 'tool':
                final_answer.append({"role": role, "content": ans})
        _googlecloudstorageservice.add_conversation(conversation_id = conve_id, conversations = final_answer)
        return final_answer
    except Exception as e:
        print(f"Error :{e}")
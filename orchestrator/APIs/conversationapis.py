from fastapi import APIRouter
from fastapi.responses import JSONResponse
from Services import SearchService, GCPStorageServiceClient

router = APIRouter()

@router.post("/refresh")
def refresh_conversation():
    try:
        _googlecloudstorageservice = GCPStorageServiceClient()
        _googlecloudstorageservice.delete_conversation(conversation_id = '891adase13e2-12128duqwd1-12')
        return JSONResponse(
                    status_code = 200,
                    content = {"message": "conversation memory has been successfully refreshed"}
                )
    except Exception as e:
        return JSONResponse(
            status_code = 500,
            content = {"message":"Error while refreshing conversation memory"}
        )
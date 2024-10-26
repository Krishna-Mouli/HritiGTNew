import logging
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from typing import List
import os
from Services import Ingestion
import asyncio

router = APIRouter()
ALLOWED_EXTENSIONS = {".txt", ".pdf", ".docx"}
MAX_FILE_SIZE = 5 * 1024 * 1024

@router.post("/apps/{app_id}")
async def ingest_index_files(app_id: str, files: List[UploadFile] = File(...)) :    
    if len(files) > 3:
        raise HTTPException(status_code=400, detail="You can upload a maximum of 3 files at once.")
    
    file_contents = []
    for file in files:       
        extension = os.path.splitext(file.filename)[1]
        if extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=400, detail=f"File type {extension} is not allowed.")
        content = await file.read()
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail=f"File {file.filename} exceeds the size limit. Keep it under 5Mb")
        file_contents.append((content, file.filename, file))        
    _ingestion = Ingestion()
    tasks = [_ingestion.Upload_and_Vectorize(file_bytes = content, app_id=app_id, filename=filename, file = file)
         for content, filename, file in file_contents]
    results = await asyncio.gather(*tasks)
    return JSONResponse(
        status_code = 200,
        content = f"Files processed successfully.\n details: {results}"
    )
    

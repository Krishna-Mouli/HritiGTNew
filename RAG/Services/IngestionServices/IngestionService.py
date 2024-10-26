from fastapi import UploadFile
from ..GoogleCloudServices import GCPStorageServiceClient
from ..AIServices import OpenAIServices
from ..VectorStoreServices import PineConeService
from Utils import Extractor, get_chunks
from Data import Chunkers

from typing import List
import asyncio
import uuid


class Ingestion:
    def __init__(self):
        self._gcp_storage_service = GCPStorageServiceClient()
        self._openai_service = OpenAIServices()
        self._pinecone_service = PineConeService()

    async def Upload_and_Vectorize(self, file_bytes: bytes, app_id: str, filename: str, file: UploadFile):
        #uploading file to google cloud service
        try:
            public_url = await self._gcp_storage_service.add_files(app_id = app_id, filename = filename, file = file)
        except Exception as e:
            return {"file": filename, "status": "failed at uploading to GCP", "error": str(e)}
        
        #calling azrre form recognition service
        try:
            content = Extractor().extract(file_bytes)
        except Exception as e:
            return {"file":filename, "status": "failed at extracting content", "error": str(e)}

        chunks = get_chunks(chunking_logic = Chunkers.BASIC_CHUNKER, content = content)

        try:
            vectors = await self.process_chunks(chunks = chunks, filename = filename, app_id = app_id, public_url = public_url)
        except Exception as e:
            return {"file": filename, "status": "failed at creating vectors", "error": str(e)}
        
        try:
            self._pinecone_service.upsert_vectors(vectors)
        except Exception as e:
            return {"file": filename, "status": "failed at uploading vectors", "error": str(e)}
        
        return {"file":filename, "status":"Completely Processd successfully"}



    async def process_chunks(self, chunks: List[str], filename: str, app_id: str, public_url: str):        
        embedding_tasks = []
        for chunk in chunks:
            task = self._openai_service.EmbeddingsOpenAI(text=chunk)
            embedding_tasks.append(task)

        vectors = await asyncio.gather(*embedding_tasks)       
        return [{
            "id": str(uuid.uuid4()),
            "values": vector,
            "metadata": {
                "filename": filename,
                "appid": app_id,
                "filepath": public_url,
                "chunk_content": chunk
            }
        } for vector, chunk in zip(vectors, chunks)]       
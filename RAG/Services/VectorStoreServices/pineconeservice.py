from pinecone import Pinecone
import os

class PineConeService:
    def __init__(self):
        self.api_key = os.environ.get("PineconeKey")
        self.pc = Pinecone(api_key = self.api_key)
        self.index = self.pc.Index("hriti-vectors")

    def upsert_vectors(self, vectors):
        try:
            self.index.upsert(
                vectors = vectors,
                namespace= "hriti-default"
            )
        except Exception as e:
            print(f"Failed to upsert {e}")
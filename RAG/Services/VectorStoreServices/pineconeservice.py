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

    def get_vectors(self, target_vectors, app_id: str):
        try:
            response = self.index.query(
            namespace = "hriti-default",
            vector = target_vectors,
            top_k = 5,
            include_values = True,
            include_metadata = True,
            filter={"appid": {"$eq": app_id}}
            )
            return (response.matches)
        except Exception as e:
            print(f"Failed to fetch data due to {e}") 
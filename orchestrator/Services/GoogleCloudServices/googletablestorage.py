from google.cloud import datastore
from typing import Optional, List, Type
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

class GCPTableStorageServiceClient():
    def __init__(self, model: Type[BaseModel]):
        self.model = model
        self.kind = model.__name__
        self.client = datastore.Client()

    def upsert_data(self, data: BaseModel) -> None:
        key = self.client.key(self.kind, data.entity_id) if data.entity_id else self.client.key(self.kind)
        entity = datastore.Entity(key=key)          
        entity.update(data.model_dump(exclude={"entity_id"})) 
        self.client.put(entity)
        print(f"Upserted entity with key: {entity.key.id or entity.key.name}")

    def update_data(self, entity_id: str, updates: dict) -> None:
        key = self.client.key(self.kind, entity_id)
        entity = self.client.get(key)

        if not entity:
            print(f"Entity with ID {entity_id} does not exist.")
            return

        entity.update(updates)
        self.client.put(entity)
        print(f"Updated entity with key: {entity_id}")

    def get_all_data(self) -> List[BaseModel]:
       query = self.client.query(kind=self.kind)
       results = list(query.fetch())
       return [self.model(entity_id=result.key.id, **result) for result in results]
    
    def delete_data(self, entity_id: str) -> None:
        key = self.client.key(self.kind, entity_id)
        self.client.delete(key)
        print(f"Deleted entity with key: {entity_id}")
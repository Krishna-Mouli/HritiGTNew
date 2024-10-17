from pydantic import BaseModel, Field
from typing import Optional, List

class ConferenceRoomData(BaseModel):   
    entity_id: Optional[str] = None
    conference_room_id: int
    occupency_limit: int
    reserved_for: str
    projector: bool
    location: str

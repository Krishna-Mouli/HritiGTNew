from pydantic import BaseModel, Field
from typing import Optional, List

class ConferenceRoomBookingData(BaseModel):   
    entity_id: Optional[str] = None
    booking_id: Optional[str] = None
    conference_room_number: str
    user_id: str
    user_name: str
    date: str
    starttime: str
    endtime: str
    duration: str
    purpose: str
    phone_number: str

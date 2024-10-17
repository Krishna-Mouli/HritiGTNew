from pydantic import BaseModel, Field
from typing import Optional, List

class ServiceNowTicketDetails(BaseModel):   
    entity_id: Optional[str] = None
    ticket_id: str
    ticket_description: str
    ticket_category: str

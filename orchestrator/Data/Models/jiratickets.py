from pydantic import BaseModel, Field
from typing import Optional, List

class JiraTicketDetails(BaseModel):   
    entity_id: Optional[str] = None
    jira_ticket_id: str
    ticket_description: str
    ticket_issue_type: str

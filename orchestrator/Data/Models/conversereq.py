from pydantic import BaseModel

class ConverseRequest(BaseModel):
    message: str
    converseid: str
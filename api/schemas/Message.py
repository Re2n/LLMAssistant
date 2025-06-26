from pydantic import BaseModel


class MessageCreate(BaseModel):
    chat_id: int
    text: str

class MessageUpdate(BaseModel):
    id: int
    response_text: str
    status: str
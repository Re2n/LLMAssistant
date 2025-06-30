from pydantic import BaseModel


class MessageCreate(BaseModel):
    chat_id: int
    text: str

class MessageUpdate(BaseModel):
    response_text: str
    status: str

class MessageUpdateStatus(BaseModel):
    status: str
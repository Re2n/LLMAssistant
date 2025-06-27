from pydantic import BaseModel


class MessageCreate(BaseModel):
    chat_id: int
    text: str

class MessageUpdate(BaseModel):
    id: int
    response_text: str | None
    status: str

class MessageUpdateStatus(BaseModel):
    id: int
    status: str

class MessageRepeat(BaseModel):
    id: int
    chat_id: int
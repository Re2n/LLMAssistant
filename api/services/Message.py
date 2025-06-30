from sqlalchemy.ext.asyncio import AsyncSession

from config.Database import query
from repositories.Message import MessageRepository
from schemas.Message import MessageCreate, MessageUpdate


class MessageService:
    def __init__(self, repository: MessageRepository):
        self.repository = repository

    async def create_message(self, session: AsyncSession, message: MessageCreate):
        new_message = await self.repository.create(session, message.chat_id, message.text)
        return new_message

    async def update_message(self, session: AsyncSession, msg_id, message: MessageUpdate):
        msg = await self.repository.get_by_id(session, msg_id)
        if msg is None:
            return msg
        return await self.repository.update(session, msg_id, message)

    async def get_history(self, session: AsyncSession, chat_id: int):
        msgs = await self.repository.get_history(session, chat_id)
        history = []
        for msg in msgs:
            history.append({"role": "user", "content": "Вопрос:" + msg.text + "Ответ: " + (
                msg.response_text if msg.response_text is not None else "")})
        return history

    async def get_by_id(self, session: AsyncSession, msg_id: int):
        msg = await self.repository.get_by_id(session, msg_id)
        return msg

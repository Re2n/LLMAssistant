from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.sync import update

from models.Message import Message
from schemas.Message import MessageUpdate, MessageUpdateStatus


class MessageRepository:
    model = Message

    async def create(self, session: AsyncSession, chat_id: int, text: str) -> Message:
        new_message = self.model(chat_id=chat_id, text=text)
        session.add(new_message)
        await session.commit()
        return new_message

    async def get_by_id(self, session: AsyncSession, msg_id: int) -> Message:
        stmt = select(self.model).where(self.model.id == msg_id)
        res = await session.execute(stmt)
        return res.scalar_one_or_none()

    async def update(self, session: AsyncSession, msg_id: int, message: MessageUpdate | MessageUpdateStatus) -> Message | None:
        msg = await self.get_by_id(session, msg_id)
        msg_dict = message.model_dump(exclude_unset=True, exclude_none=True)
        for field, value in msg_dict.items():
            setattr(msg, field, value)

        session.add(msg)
        await session.commit()
        return msg

    async def get_history(self, session: AsyncSession, chat_id: int):
        stmt = select(Message).where(self.model.chat_id == chat_id).order_by(Message.created_at.desc()).limit(10)
        res = await session.execute(stmt)
        return res.scalars().all()

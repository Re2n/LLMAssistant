from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.templating import Jinja2Templates
from sqladmin import Admin, ModelView, action
from fastapi import Request

from config.Database import db
from models.Message import Message
from fastapi.responses import RedirectResponse

templates = Jinja2Templates(directory="templates")


async def send_telegram_message(tg_id: str, text: str):
    print(f"Отправлено в Telegram {tg_id}: {text}")

class PendingMessageAdmin(ModelView, model=Message):
    name = "Сообщения на модерации"
    name_plural = "Сообщения на модерации"

    def list_query(self, request: Request) -> Select:
        return select(Message).where(Message.status == "pending")

    column_list = [
        "id",
        "tg_id",
        "text",
        "created_at",
        "response_text"
    ]
    column_default_sort = [("created_at", True)]

    # Кастомные действия
    actions = ["approve", "reject", "edit_dialog"]

    @action(
        name="approve",
        label="Принять",
        add_in_list=True,
        add_in_detail = True
    )
    async def approve_action(self, request: Request):
        msg_id = request.query_params.get("pks")
        session = AsyncSession(db.engine)
        try:
            message = await session.get(Message, int(msg_id))
            message.status = "approved"
            if message.chat_id and message.response_text:
                await send_telegram_message(str(message.chat_id), str(message.response_text))
            await session.commit()
            return RedirectResponse(url=request.url_for("admin:list", identity="message"))
        finally:
            await session.close()

    @action(
        name="reject",
        label="Отклонить",
        add_in_list=True,
        add_in_detail=True
    )
    async def reject_action(self, request: Request):
        msg_id = request.query_params.get("pks")
        session = AsyncSession(db.engine)
        try:
            message = await session.get(Message, int(msg_id))
            message.status = "rejected"
            await session.commit()
            return RedirectResponse(url=request.url_for("admin:list", identity="message"))
        finally:
            await session.close()

    @action(
        name="view_dialog",
        label="История",
        add_in_list=True,
        add_in_detail=True
    )
    async def view_dialog_action(self, request: Request):
        msg_id = request.query_params.get("pks")
        session = AsyncSession(db.engine)
        try:
            message = await session.get(Message, int(msg_id))

            # Получаем все сообщения пользователя
            stmt = (
                select(Message)
                .where(Message.chat_id == message.chat_id)
                .order_by(Message.created_at.asc())  # Хронологический порядок
            )
            result = await session.execute(stmt)
            messages = result.scalars().all()

            context = {
                "request": request,
                "chat_id": message.chat_id,
                "messages": messages,
            }

            return templates.TemplateResponse(
                "dialog.html",
                context
            )
        finally:
            await session.close()
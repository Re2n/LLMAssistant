import aiohttp
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.templating import Jinja2Templates
from sqladmin import Admin, ModelView, action
from fastapi import Request

from config.Database import db
from models.Message import Message
from fastapi.responses import RedirectResponse

from schemas.Message import MessageUpdateStatus
from utils.depends import message_service

templates = Jinja2Templates(directory="templates")


async def send_telegram_message(tg_id: str, text: str):
    print(f"Отправлено в Telegram {tg_id}: {text}")


class PendingMessageAdmin(ModelView, model=Message):
    name = "Сообщения на модерации"
    name_plural = "Сообщения на модерации"
    can_create = False
    can_delete = False

    def list_query(self, request: Request) -> Select:
        return select(Message).where(Message.status == "pending")

    column_list = [
        "chat_id",
        "text",
        "response_text",
        "created_at",
    ]
    column_labels = {Message.chat_id: "Идендификатор пользователя", Message.text: "Сообщение",
                     Message.response_text: "Ответ LLM", Message.created_at: "Дата получения", Message.status: "Статус"}
    column_details_exclude_list = [Message.created_at, Message.id]
    column_default_sort = [("created_at", True)]
    form_rules = ["text", "response_text"]

    # Кастомные действия
    actions = ["approve", "reject", "edit_dialog"]

    @action(
        name="approve",
        label="Принять",
        add_in_list=True,
        add_in_detail=True
    )
    async def approve_action(self, request: Request):
        msg_id = request.query_params.get("pks")
        async for session in db.session_getter():
            try:
                msg = await message_service.get_by_id(session, msg_id)
                await message_service.update_message(session, MessageUpdateStatus(id=msg_id, status="approved"))
                await send_telegram_message(str(msg.chat_id), str(msg.response_text))
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
        async for session in db.session_getter():
            try:
                msg = await message_service.get_by_id(session, msg_id)
                await message_service.update_message(session, MessageUpdateStatus(id=msg_id, status="rejected"))
                payload = {
                    "id": msg_id,
                    "chat_id": str(msg.chat_id)
                }
                async with aiohttp.ClientSession() as aio_session:
                    await aio_session.post("http://localhost:5466/create", json=payload)
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

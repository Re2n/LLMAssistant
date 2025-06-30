from typing import Annotated, List

from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from config.Database import db, query
from schemas.Message import MessageCreate, MessageUpdate, MessageUpdateStatus
from utils.depends import message_service, ollama_service
from utils.prompt import get_prompt

message_router = APIRouter(tags=["Message"])


@message_router.post("/create")
async def create_message(session: Annotated[AsyncSession, Depends(db.session_getter)],
                         message: MessageCreate,
                         background_tasks: BackgroundTasks):
    res = await message_service.create_message(session, message)
    msgs = await message_service.get_history(session, res.chat_id)
    prompt = await get_prompt(msgs[1:], msgs[0]['content'])
    background_tasks.add_task(ollama_service.query_ollama, prompt, res.id)
    return res


@message_router.post("/repeat/{msg_id}")
async def repeat_message(session: Annotated[AsyncSession, Depends(db.session_getter)], msg_id: int,
                         background_tasks: BackgroundTasks):
    msg = await message_service.get_by_id(session, msg_id)
    msgs = await message_service.get_history(session, msg.chat_id)
    prompt = await get_prompt(msgs[1:], msgs[0]['content'])
    print(prompt)
    background_tasks.add_task(ollama_service.query_ollama, prompt, msg.id)
    return msg


@message_router.patch("/update_message/{msg_id}")
async def update_message(session: Annotated[AsyncSession, Depends(db.session_getter)], msg_id: int,
                         message: MessageUpdate | MessageUpdateStatus):
    return await message_service.update_message(session, msg_id, message)

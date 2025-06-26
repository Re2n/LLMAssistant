from typing import Annotated, List

from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from config.Database import db, query
from schemas.Message import MessageCreate, MessageUpdate
from utils.depends import message_service, ollama_service
from utils.prompt import get_prompt

message_router = APIRouter(tags=["Message"])


@message_router.post("/create")
async def create_message(session: Annotated[AsyncSession, Depends(db.session_getter)], message: MessageCreate,
                         background_tasks: BackgroundTasks):
    res = await message_service.create_message(session, message)
    msgs = await message_service.get_history(session, res.chat_id)
    prompt = await get_prompt(msgs[1:], msgs[0]['content'])
    print(prompt)
    background_tasks.add_task(ollama_service.query_ollama, prompt, res.id)
    return res


@message_router.patch("/update_response_text")
async def update_response_text(session: Annotated[AsyncSession, Depends(db.session_getter)], message: MessageUpdate):
    await message_service.update_response_text(session, message)

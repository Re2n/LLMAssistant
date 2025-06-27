import aiohttp
from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text)
async def message_with_text(message: Message):
    await message.answer("Ваше сообщение на обработке, скоро вы получите свой ответ!")
    payload = {
        "chat_id": message.chat.id,
        "text": message.text
    }
    async with aiohttp.ClientSession() as session:
        await session.post("http://localhost:5466/create", json=payload)
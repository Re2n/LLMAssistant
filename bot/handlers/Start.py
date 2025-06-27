from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Я бот с локальной LLM (OLLAMA). Задайте мне вопрос!"
    )
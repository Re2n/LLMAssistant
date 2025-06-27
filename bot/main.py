import asyncio
from aiogram import Bot, Dispatcher

from config.Config import bot_token
from handlers import Start, Message

# Запуск бота
async def main():
    bot = Bot(token=bot_token)
    dp = Dispatcher()
    dp.include_routers(Start.router, Message.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())